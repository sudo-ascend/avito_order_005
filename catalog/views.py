from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .forms import MergeConfirmationForm, PriceUploadForm
from .models import GalleryItem, PlantProduct, PriceUpload, Review, SiteConfiguration
from .services.prices import HEADERS, apply_price_upload, create_price_upload_from_file, export_products_to_workbook, reject_price_upload


FAVORITES_SESSION_KEY = "favorite_product_ids"


def get_site_configuration():
    config = SiteConfiguration.objects.first()
    if config is None:
        config = SiteConfiguration.objects.create()
    return config


def get_favorite_product_ids(request):
    raw_ids = request.session.get(FAVORITES_SESSION_KEY, [])
    normalized_ids = []
    for raw_id in raw_ids:
        try:
            normalized_ids.append(int(raw_id))
        except (TypeError, ValueError):
            continue
    if normalized_ids != raw_ids:
        request.session[FAVORITES_SESSION_KEY] = normalized_ids
    return normalized_ids


def get_favorites_context(request):
    favorite_product_ids = get_favorite_product_ids(request)
    return {
        "favorite_product_ids": favorite_product_ids,
        "favorite_product_count": len(favorite_product_ids),
    }


@ensure_csrf_cookie
def home(request):
    config = get_site_configuration()
    context = {
        "config": config,
        "products": PlantProduct.objects.filter(is_published=True).order_by("variety_name", "article")[:12],
        "gallery_items": GalleryItem.objects.filter(is_published=True),
        "reviews": Review.objects.filter(is_published=True),
    }
    context.update(get_favorites_context(request))
    return render(request, "catalog/home.html", context)


@ensure_csrf_cookie
def favorite_products(request):
    config = get_site_configuration()
    favorite_product_ids = get_favorite_product_ids(request)
    order_map = {product_id: index for index, product_id in enumerate(favorite_product_ids)}
    products = list(PlantProduct.objects.filter(is_published=True, id__in=favorite_product_ids))
    products.sort(key=lambda product: order_map.get(product.id, 10**9))

    context = {
        "config": config,
        "products": products,
    }
    context.update(get_favorites_context(request))
    return render(request, "catalog/favorite_products.html", context)


@require_POST
def toggle_favorite_product(request, pk: int):
    product = get_object_or_404(PlantProduct.objects.filter(is_published=True), pk=pk)
    favorite_product_ids = get_favorite_product_ids(request)

    if product.pk in favorite_product_ids:
        favorite_product_ids.remove(product.pk)
        is_favorite = False
    else:
        favorite_product_ids.append(product.pk)
        is_favorite = True

    request.session[FAVORITES_SESSION_KEY] = favorite_product_ids
    request.session.modified = True

    return JsonResponse(
        {
            "ok": True,
            "product_id": product.pk,
            "is_favorite": is_favorite,
            "favorite_count": len(favorite_product_ids),
        }
    )


@staff_member_required
def price_upload_registry(request):
    config = get_site_configuration()
    form = PriceUploadForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        update_requested = form.cleaned_data["should_update_prices"] == "yes"
        try:
            price_upload = create_price_upload_from_file(
                uploaded_file=form.cleaned_data["file"],
                user=request.user,
                update_requested=update_requested,
            )
        except ValueError as error:
            form.add_error("file", str(error))
        else:
            if not update_requested:
                messages.success(request, "Файл сохранен в реестре без обновления базы.")
                return redirect("catalog:price_upload_registry")

            return redirect("catalog:price_upload_confirm", pk=price_upload.pk)

    uploads = PriceUpload.objects.all()
    paginator = Paginator(uploads, 8)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "config": config,
        "form": form,
        "page_obj": page_obj,
    }
    context.update(get_favorites_context(request))
    return render(request, "catalog/price_upload_registry.html", context)


@staff_member_required
def price_upload_confirm(request, pk: int):
    config = get_site_configuration()
    price_upload = get_object_or_404(PriceUpload, pk=pk)
    if not price_upload.update_requested:
        raise Http404("Для этого файла merge не запрашивался.")

    form = MergeConfirmationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["confirm_merge"] == "yes":
            applied_count = apply_price_upload(price_upload)
            messages.success(request, f"Изменения применены. Обработано товаров: {applied_count}.")
        else:
            reject_price_upload(price_upload)
            messages.info(request, "Merge отменен. В реестре сохранена отметка is_merged = False.")
        return redirect("catalog:price_upload_registry")

    label_map = {value: key for key, value in HEADERS.items()}
    raw_changes = price_upload.change_summary.get("changes_per_field", {})
    changes = [(label_map.get(field, field), count) for field, count in raw_changes.items()]
    context = {
        "config": config,
        "price_upload": price_upload,
        "form": form,
        "changes": changes,
        "new_records": price_upload.change_summary.get("new_records", 0),
    }
    context.update(get_favorites_context(request))
    return render(request, "catalog/price_upload_confirm.html", context)


@staff_member_required
def price_upload_download(request, pk: int):
    price_upload = get_object_or_404(PriceUpload, pk=pk)
    return FileResponse(price_upload.file.open("rb"), as_attachment=True, filename=price_upload.display_filename)


@staff_member_required
def export_database_excel(request):
    workbook_stream = export_products_to_workbook()
    filename = f"{slugify(get_site_configuration().brand_name) or 'catalog'}-database.xlsx"
    return FileResponse(workbook_stream, as_attachment=True, filename=filename)
