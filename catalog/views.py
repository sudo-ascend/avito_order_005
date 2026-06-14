import json
from datetime import datetime
from urllib.parse import urlsplit

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import http_date

from .models import Benefit, GalleryItem, OrderStep, Review, SiteConfiguration


def get_site_configuration():
    config = SiteConfiguration.objects.first()
    if config is None:
        config = SiteConfiguration.objects.create()
    return config


def get_absolute_url(request, path_or_url):
    if not path_or_url:
        return ""
    absolute_url = request.build_absolute_uri(path_or_url)
    if settings.DEBUG:
        return absolute_url.replace("https://", "http://", 1)
    return absolute_url


def get_canonical_url(request, config):
    canonical_url = request.build_absolute_uri(reverse("catalog:home"))
    if settings.DEBUG:
        return canonical_url.replace("https://", "http://", 1)
    return canonical_url


def get_site_last_modified():
    file_candidates = (
        settings.BASE_DIR / "db.sqlite3",
        settings.BASE_DIR / "catalog" / "views.py",
        settings.BASE_DIR / "catalog" / "models.py",
        settings.BASE_DIR / "catalog" / "templates" / "catalog" / "base.html",
        settings.BASE_DIR / "catalog" / "templates" / "catalog" / "home.html",
    )
    mtimes = [path.stat().st_mtime for path in file_candidates if path.exists()]
    if not mtimes:
        return None
    return datetime.fromtimestamp(max(mtimes), tz=timezone.get_current_timezone())


def build_image_entries(request, config, gallery_items):
    raw_images = [
        {
            "loc": get_absolute_url(request, config.social_image_url),
            "caption": config.social_image_alt or config.site_title,
            "title": config.brand_name,
        },
        {
            "loc": get_absolute_url(request, config.hero_image_url),
            "caption": config.hero_title,
            "title": config.brand_name,
        },
    ]
    raw_images.extend(
        {
            "loc": get_absolute_url(request, item.display_image_url),
            "caption": item.image_alt or item.text,
            "title": item.title,
        }
        for item in gallery_items
        if item.display_image_url
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


def build_structured_data(request, config, canonical_url, page_last_modified, reviews):
    organization_id = f"{canonical_url}#organization"
    website_id = f"{canonical_url}#website"
    webpage_id = f"{canonical_url}#webpage"
    logo_url = get_absolute_url(request, config.logo_url)
    social_image_url = get_absolute_url(request, config.social_image_url)
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
        "address": {
            "@type": "PostalAddress",
            "addressLocality": config.contact_city,
            "addressCountry": "RU",
        },
        "areaServed": config.contact_city,
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
        "primaryImageOfPage": social_image_url,
    }
    if page_last_modified:
        webpage_schema["dateModified"] = page_last_modified.isoformat()

    return [
        json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
        for schema in (organization_schema, website_schema, webpage_schema)
    ]


def build_home_context(request):
    config = get_site_configuration()
    benefits = list(Benefit.objects.filter(is_published=True))
    gallery_items = list(GalleryItem.objects.filter(is_published=True))
    order_steps = list(OrderStep.objects.filter(is_published=True))
    reviews = list(Review.objects.filter(is_published=True))
    canonical_url = get_canonical_url(request, config)
    page_last_modified = get_site_last_modified()

    seo_context = {
        "canonical_url": canonical_url,
        "meta_robots": config.meta_robots,
        "og_image_url": get_absolute_url(request, config.social_image_url),
        "og_image_alt": config.social_image_alt or config.site_title,
        "hero_image_url": get_absolute_url(request, config.hero_image_url),
        "logo_url": get_absolute_url(request, config.logo_url),
        "page_last_modified": page_last_modified,
        "sitemap_url": get_absolute_url(request, reverse("catalog:sitemap")),
        "structured_data": build_structured_data(
            request=request,
            config=config,
            canonical_url=canonical_url,
            page_last_modified=page_last_modified,
            reviews=reviews,
        ),
    }

    return {
        "config": config,
        "benefits": benefits,
        "gallery_items": gallery_items,
        "order_steps": order_steps,
        "reviews": reviews,
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
    config = get_site_configuration()
    canonical_url = get_canonical_url(request, config)
    response = render(
        request,
        "catalog/robots.txt",
        {
            "sitemap_url": get_absolute_url(request, reverse("catalog:sitemap")),
            "host": urlsplit(canonical_url).netloc or request.get_host(),
        },
        content_type="text/plain; charset=utf-8",
    )
    response["X-Robots-Tag"] = "noindex, follow"
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
            "images": build_image_entries(request, context["config"], context["gallery_items"]),
        }
    ]
    return render(
        request,
        "catalog/sitemap.xml",
        {"pages": pages},
        content_type="application/xml; charset=utf-8",
    )
