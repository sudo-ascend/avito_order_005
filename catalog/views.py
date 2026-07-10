import json
import mimetypes
from urllib.parse import urljoin, urlsplit

from django.conf import settings
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.http import http_date

from .models import Benefit, FAQItem, GalleryItem, OrderStep, PlantProduct, Review, SiteConfiguration


PAGE_NOINDEX_DIRECTIVES = "noindex, nofollow, noarchive"
TECHNICAL_NOINDEX_DIRECTIVES = "noindex, follow"
TRACKING_CLEAN_PARAMS = "utm_source&utm_medium&utm_campaign&utm_term&utm_content&utm_id&gclid&yclid&ysclid&fbclid"


def get_site_configuration():
    config = SiteConfiguration.objects.first()
    if config is None:
        config = SiteConfiguration.objects.create()
    return config


def normalize_host(host):
    return host.split(":", 1)[0].strip().lower()


def get_site_host():
    return normalize_host(urlsplit(settings.SITE_URL).netloc)


def build_public_url(path_or_url):
    if not path_or_url:
        return ""
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    return urljoin(f"{settings.SITE_URL}/", path_or_url.lstrip("/"))


def is_primary_host_request(request):
    return normalize_host(request.get_host()) == get_site_host()


def get_canonical_url():
    return build_public_url(reverse("catalog:home"))


def get_page_robots(request, config):
    if settings.SEO_NOINDEX or not is_primary_host_request(request):
        return PAGE_NOINDEX_DIRECTIVES
    return config.meta_robots


def get_site_last_modified():
    last_modified_values = [
        SiteConfiguration.objects.order_by("-updated_at").values_list("updated_at", flat=True).first(),
        Benefit.objects.filter(is_published=True).order_by("-updated_at").values_list("updated_at", flat=True).first(),
        GalleryItem.objects.filter(is_published=True).order_by("-updated_at").values_list("updated_at", flat=True).first(),
        OrderStep.objects.filter(is_published=True).order_by("-updated_at").values_list("updated_at", flat=True).first(),
        PlantProduct.objects.filter(is_published=True).order_by("-updated_at").values_list("updated_at", flat=True).first(),
        Review.objects.filter(is_published=True).order_by("-updated_at").values_list("updated_at", flat=True).first(),
        FAQItem.objects.filter(is_published=True).order_by("-updated_at").values_list("updated_at", flat=True).first(),
    ]
    return max((value for value in last_modified_values if value is not None), default=None)


def build_image_entries(config, gallery_items, plant_products):
    raw_images = [
        {
            "loc": build_public_url(config.social_image_url),
            "caption": config.social_image_alt or config.site_title,
            "title": config.brand_name,
        },
        {
            "loc": build_public_url(config.hero_image_url),
            "caption": config.hero_title,
            "title": config.brand_name,
        },
    ]
    raw_images.extend(
        {
            "loc": build_public_url(item.display_image_url),
            "caption": item.image_alt or item.text,
            "title": item.title,
        }
        for item in gallery_items
        if item.display_image_url
    )
    raw_images.extend(
        {
            "loc": build_public_url(product.display_image_url),
            "caption": product.image_alt,
            "title": product.title,
        }
        for product in plant_products
        if product.display_image_url
    )

    deduped = []
    seen = set()
    for image in raw_images:
        location = image["loc"]
        if not location or location in seen:
            continue
        seen.add(location)
        deduped.append(image)
    return deduped


def build_structured_data(
    config,
    canonical_url,
    page_last_modified,
    reviews,
    benefits,
    gallery_items,
    order_steps,
    faq_items,
    plant_products,
):
    organization_id = f"{canonical_url}#organization"
    website_id = f"{canonical_url}#website"
    webpage_id = f"{canonical_url}#webpage"
    breadcrumb_id = f"{canonical_url}#breadcrumbs"
    logo_url = build_public_url(config.logo_url)
    social_image_url = build_public_url(config.social_image_url)
    review_items = list(reviews[:3])
    same_as = [url for url in (config.whatsapp_url, config.max_url, config.telegram_url) if url]

    organization_schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": organization_id,
        "name": config.brand_name,
        "url": canonical_url,
        "description": config.meta_description,
        "image": social_image_url,
        "logo": logo_url,
        "telephone": config.contact_phone,
        "email": config.contact_email,
        "priceRange": getattr(config, "business_price_range", "$$"),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": getattr(config, "address_street", ""),
            "addressLocality": config.contact_city,
            "addressRegion": getattr(config, "contact_region", ""),
            "addressCountry": "RU",
        },
        "areaServed": getattr(config, "contact_region", config.contact_city),
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "description": getattr(config, "opening_hours", ""),
            }
        ],
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "contactType": "customer support",
                "telephone": config.contact_phone,
                "email": config.contact_email,
                "availableLanguage": ["ru"],
                "areaServed": "RU",
            }
        ],
    }
    if same_as:
        organization_schema["sameAs"] = same_as
    if reviews:
        organization_schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(config.reviews_rating),
            "reviewCount": len(reviews),
            "bestRating": "5",
            "worstRating": "1",
        }
        organization_schema["review"] = [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": review.name},
                "reviewBody": review.text,
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": str(review.rating),
                    "bestRating": "5",
                    "worstRating": "1",
                },
            }
            for review in review_items
        ]

    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": website_id,
        "url": canonical_url,
        "name": config.brand_name,
        "description": config.meta_description,
        "inLanguage": "ru-RU",
        "publisher": {"@id": organization_id},
    }

    webpage_schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": webpage_id,
        "url": canonical_url,
        "name": config.site_title,
        "description": config.meta_description,
        "inLanguage": "ru-RU",
        "isPartOf": {"@id": website_id},
        "about": {"@id": organization_id},
        "breadcrumb": {"@id": breadcrumb_id},
        "primaryImageOfPage": social_image_url,
        "mainEntity": {"@id": organization_id},
    }
    if page_last_modified:
        webpage_schema["dateModified"] = page_last_modified.isoformat()

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "@id": breadcrumb_id,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": config.brand_name,
                "item": canonical_url,
            }
        ],
    }

    schemas = [organization_schema, website_schema, webpage_schema, breadcrumb_schema]

    if benefits:
        schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "@id": f"{canonical_url}#benefits",
                "name": config.advantages_title,
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index,
                        "name": benefit.title,
                        "description": benefit.text,
                    }
                    for index, benefit in enumerate(benefits, start=1)
                ],
            }
        )

    if plant_products:
        schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "@id": f"{canonical_url}#plants",
                "name": config.plants_title,
                "description": config.plants_text,
                "numberOfItems": len(plant_products),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": index,
                        "url": f"{canonical_url}#plants",
                        "item": {
                            "@type": "Product",
                            "@id": f"{canonical_url}#plant-{product.slug}",
                            "name": product.title,
                            "alternateName": product.latin_name,
                            "description": product.description,
                            "image": build_public_url(product.display_image_url),
                            "category": "Аквариумные растения in vitro",
                            "brand": {
                                "@type": "Brand",
                                "name": config.brand_name,
                            },
                        },
                    }
                    for index, product in enumerate(plant_products, start=1)
                ],
            }
        )

    if gallery_items:
        schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "ImageGallery",
                "@id": f"{canonical_url}#gallery",
                "name": config.aquariums_title,
                "description": config.aquariums_text,
                "image": [
                    {
                        "@type": "ImageObject",
                        "contentUrl": build_public_url(item.display_image_url),
                        "name": item.title,
                        "description": item.image_alt or item.text,
                    }
                    for item in gallery_items
                    if item.display_image_url
                ],
            }
        )

    if order_steps:
        schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "HowTo",
                "@id": f"{canonical_url}#how-to-order",
                "name": config.order_title,
                "step": [
                    {
                        "@type": "HowToStep",
                        "position": index,
                        "name": step.title,
                        "text": step.text,
                    }
                    for index, step in enumerate(order_steps, start=1)
                ],
            }
        )

    if faq_items:
        schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "@id": f"{canonical_url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item.question,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": item.answer,
                        },
                    }
                    for item in faq_items
                ],
            }
        )

    return [json.dumps(schema, ensure_ascii=False, separators=(",", ":")) for schema in schemas]


def build_home_context(request):
    config = get_site_configuration()
    benefits = list(Benefit.objects.filter(is_published=True))
    gallery_items = list(GalleryItem.objects.filter(is_published=True))
    order_steps = list(OrderStep.objects.filter(is_published=True))
    reviews = list(Review.objects.filter(is_published=True))
    faq_items = list(FAQItem.objects.filter(is_published=True))
    plant_products = list(PlantProduct.objects.filter(is_published=True))
    canonical_url = get_canonical_url()
    page_last_modified = get_site_last_modified()
    seo_context = {
        "canonical_url": canonical_url,
        "meta_robots": get_page_robots(request, config),
        "meta_keywords": getattr(config, "seo_keywords", ""),
        "google_site_verification": getattr(config, "google_site_verification", ""),
        "yandex_site_verification": getattr(config, "yandex_site_verification", ""),
        "og_image_url": build_public_url(config.social_image_url),
        "og_image_alt": config.social_image_alt or config.site_title,
        "hero_image_url": build_public_url(config.hero_image_url),
        "logo_url": build_public_url(config.logo_url),
        "page_last_modified": page_last_modified,
        "sitemap_url": build_public_url(reverse("catalog:sitemap")),
        "is_indexable": is_primary_host_request(request) and not settings.SEO_NOINDEX,
        "structured_data": build_structured_data(
            config=config,
            canonical_url=canonical_url,
            page_last_modified=page_last_modified,
            reviews=reviews,
            benefits=benefits,
            gallery_items=gallery_items,
            order_steps=order_steps,
            faq_items=faq_items,
            plant_products=plant_products,
        ),
    }
    return {
        "config": config,
        "benefits": benefits,
        "gallery_items": gallery_items,
        "order_steps": order_steps,
        "reviews": reviews,
        "faq_items": faq_items,
        "plant_products": plant_products,
        "seo": seo_context,
    }


def home(request):
    context = build_home_context(request)
    response = render(request, "catalog/home.html", context)
    response["X-Robots-Tag"] = context["seo"]["meta_robots"]
    if context["seo"]["page_last_modified"]:
        response["Last-Modified"] = http_date(context["seo"]["page_last_modified"].timestamp())
    return response


def robots_txt(request):
    response = render(
        request,
        "catalog/robots.txt",
        {
            "allow_indexing": is_primary_host_request(request) and not settings.SEO_NOINDEX,
            "clean_params": TRACKING_CLEAN_PARAMS,
            "sitemap_url": build_public_url(reverse("catalog:sitemap")),
            "host": get_site_host(),
        },
        content_type="text/plain; charset=utf-8",
    )
    response["X-Robots-Tag"] = TECHNICAL_NOINDEX_DIRECTIVES
    return response


def sitemap_xml(request):
    context = build_home_context(request)
    page_last_modified = context["seo"]["page_last_modified"]
    pages = [
        {
            "loc": context["seo"]["canonical_url"],
            "lastmod": page_last_modified.date().isoformat() if page_last_modified else "",
            "changefreq": "weekly",
            "priority": "1.0",
            "alternates": [
                {"hreflang": "ru-RU", "href": context["seo"]["canonical_url"]},
                {"hreflang": "x-default", "href": context["seo"]["canonical_url"]},
            ],
            "images": build_image_entries(context["config"], context["gallery_items"], context["plant_products"]),
        }
    ]
    response = render(
        request,
        "catalog/sitemap.xml",
        {"pages": pages},
        content_type="application/xml; charset=utf-8",
    )
    response["X-Robots-Tag"] = TECHNICAL_NOINDEX_DIRECTIVES
    return response


def favicon(request):
    config = get_site_configuration()
    icon = config.favicon or config.logo
    if icon and icon.name and icon.storage.exists(icon.name):
        icon.open("rb")
        content_type, _encoding = mimetypes.guess_type(icon.name)
        response = FileResponse(icon.file, content_type=content_type or "application/octet-stream")
        response["Cache-Control"] = "no-cache"
        return response
    return HttpResponseRedirect(static("favicon.ico"))


def yandex_verification(request):
    return render(
        request,
        "catalog/yandex_4d153c26552f0309.html",
        content_type="text/html; charset=utf-8",
    )


def render_error_page(request, template_name, status_code):
    response = render(request, template_name, status=status_code)
    response["X-Robots-Tag"] = PAGE_NOINDEX_DIRECTIVES
    return response


def bad_request(request, exception):
    return render_error_page(request, "400.html", 400)


def permission_denied(request, exception):
    return render_error_page(request, "403.html", 403)


def page_not_found(request, exception):
    return render_error_page(request, "404.html", 404)


def server_error(request):
    return render_error_page(request, "500.html", 500)


def error_400_preview(request):
    return render_error_page(request, "400.html", 400)


def error_403_preview(request):
    return render_error_page(request, "403.html", 403)


def error_404_preview(request):
    return render_error_page(request, "404.html", 404)


def error_500_preview(request):
    return render_error_page(request, "500.html", 500)
