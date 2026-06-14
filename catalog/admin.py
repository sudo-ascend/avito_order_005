from pathlib import Path

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Benefit, GalleryItem, OrderStep, Review, SiteConfiguration


def render_preview(image_url: str, alt: str, *, size: int = 72):
    if not image_url:
        return "-"
    return format_html(
        '<img src="{}" alt="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:10px;border:1px solid #d8e5e0;" />',
        image_url,
        alt,
        size,
        size,
    )


PRICE_FILE_ALLOWED_EXTENSIONS = {".xlsx"}


def get_site_configuration():
    config, _created = SiteConfiguration.objects.get_or_create(pk=1)
    return config


def get_price_file_context():
    config = SiteConfiguration.objects.first()
    if config is None:
        return {
            "price_file_name": "",
            "price_file_url": "",
        }
    return {
        "price_file_name": config.price_file_name,
        "price_file_url": config.price_file_url,
    }


def update_price_file_view(request):
    if request.method != "POST":
        return redirect("admin:index")

    uploaded_file = request.FILES.get("price_file")
    if uploaded_file is None:
        messages.error(request, "Выберите Excel-файл для обновления прайса.")
        return redirect("admin:index")

    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in PRICE_FILE_ALLOWED_EXTENSIONS:
        messages.error(request, "Поддерживается только формат .xlsx.")
        return redirect("admin:index")

    config = get_site_configuration()
    if config.price_file:
        config.price_file.delete(save=False)
    config.price_file.save(uploaded_file.name, uploaded_file, save=False)
    config.price_file_original_name = uploaded_file.name
    config.save(update_fields=("price_file", "price_file_original_name"))

    messages.success(request, f"Файл с ценами обновлен: {uploaded_file.name}")
    return redirect("admin:index")


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    readonly_fields = (
        "logo_preview",
        "social_image_preview",
        "hero_image_preview",
    )
    fieldsets = (
        (
            "Бренд и SEO",
            {
                "fields": (
                    "brand_name",
                    "brand_caption",
                    "site_title",
                    "meta_description",
                    "meta_robots",
                    "logo",
                    "logo_preview",
                    "social_image",
                    "social_image_alt",
                    "social_image_preview",
                    "footer_text",
                )
            },
        ),
        (
            "Навигация",
            {
                "fields": (
                    "nav_about_label",
                    "nav_advantages_label",
                    "nav_plants_label",
                    "nav_aquariums_label",
                    "nav_reviews_label",
                    "nav_contacts_label",
                    "header_contact_button_text",
                )
            },
        ),
        (
            "Первый экран",
            {
                "fields": (
                    "hero_eyebrow",
                    "hero_title",
                    "hero_lead",
                    "hero_primary_button_text",
                    "hero_secondary_button_text",
                    "hero_feature_1",
                    "hero_feature_2",
                    "hero_feature_3",
                    "hero_feature_4",
                    "hero_image",
                    "hero_image_preview",
                )
            },
        ),
        (
            "О нас",
            {
                "fields": (
                    "about_eyebrow",
                    "about_title",
                    "about_body_1",
                    "about_body_2",
                    "about_panel_title",
                    "about_panel_text",
                )
            },
        ),
        (
            "Блок преимуществ",
            {
                "description": "Карточки этого блока редактируются отдельно в списке «Преимущества».",
                "fields": (
                    "advantages_eyebrow",
                    "advantages_title",
                    "advantages_text",
                )
            },
        ),
        (
            "Растения",
            {
                "fields": (
                    "plants_eyebrow",
                    "plants_title",
                )
            },
        ),
        (
            "Галерея, отзывы и контакты",
            {
                "fields": (
                    "aquariums_eyebrow",
                    "aquariums_title",
                    "aquariums_text",
                    "order_eyebrow",
                    "order_title",
                    "reviews_eyebrow",
                    "reviews_title",
                    "reviews_rating",
                    "contacts_eyebrow",
                    "contacts_title",
                    "contacts_text",
                    "contact_phone",
                    "contact_phone_display",
                    "contact_email",
                    "contact_city",
                    "contacts_call_button_text",
                    "contacts_email_button_text",
                    "contacts_whatsapp_button_text",
                    "contacts_max_button_text",
                    "contacts_telegram_button_text",
                    "whatsapp_url",
                    "max_url",
                    "telegram_url",
                )
            },
        ),
    )

    def changelist_view(self, request, extra_context=None):
        config = get_site_configuration()
        return HttpResponseRedirect(reverse("admin:catalog_siteconfiguration_change", args=[config.pk]))

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def logo_preview(self, obj):
        return render_preview(obj.logo_url, obj.brand_name)

    logo_preview.short_description = "Превью логотипа"

    def hero_image_preview(self, obj):
        return render_preview(obj.hero_image_url, obj.hero_title, size=180)

    hero_image_preview.short_description = "Превью первого экрана"

    def social_image_preview(self, obj):
        return render_preview(obj.social_image_url, obj.social_image_alt or obj.site_title, size=180)

    social_image_preview.short_description = "Превью для соцсетей"

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ("icon", "title", "sort_order", "is_published")
    list_editable = ("sort_order", "is_published")
    ordering = ("sort_order", "id")
    fields = ("icon", "title", "text", "sort_order", "is_published")


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "title", "sort_order", "is_published")
    list_editable = ("sort_order", "is_published")
    ordering = ("sort_order", "id")
    readonly_fields = ("image_preview_large",)
    fieldsets = (
        (
            "Содержимое",
            {
                "fields": (
                    "title",
                    "text",
                    "image",
                    "image_preview_large",
                    "image_alt",
                )
            },
        ),
        (
            "Публикация",
            {
                "fields": (
                    "sort_order",
                    "is_published",
                )
            },
        ),
    )

    def image_preview(self, obj):
        return render_preview(obj.display_image_url, obj.title, size=52)

    image_preview.short_description = "Фото"

    def image_preview_large(self, obj):
        return render_preview(obj.display_image_url, obj.title, size=220)

    image_preview_large.short_description = "Превью"


@admin.register(OrderStep)
class OrderStepAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order", "is_published")
    list_editable = ("sort_order", "is_published")
    ordering = ("sort_order", "id")
    fields = ("title", "text", "sort_order", "is_published")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "sort_order", "is_published")
    list_editable = ("rating", "sort_order", "is_published")
    ordering = ("sort_order", "id")
    fields = ("name", "rating", "text", "sort_order", "is_published")


UserModel = get_user_model()
if UserModel in admin.site._registry:
    admin.site.unregister(UserModel)
if Group in admin.site._registry:
    admin.site.unregister(Group)

admin.site.site_header = "Админка Aquaklon"
admin.site.site_title = "Админка Aquaklon"
admin.site.index_title = "Управление содержимым сайта"
admin.site.site_url = "/"

_admin_site_get_urls = admin.site.get_urls
_admin_site_each_context = admin.site.each_context


def custom_admin_urls():
    return [
        path(
            "price-file/update/",
            admin.site.admin_view(update_price_file_view),
            name="catalog_update_price_file",
        ),
        *_admin_site_get_urls(),
    ]


def custom_admin_each_context(request):
    context = _admin_site_each_context(request)
    context.update(get_price_file_context())
    return context


admin.site.get_urls = custom_admin_urls
admin.site.each_context = custom_admin_each_context
