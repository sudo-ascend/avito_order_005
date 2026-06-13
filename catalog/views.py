import json
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlsplit

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import http_date

from .models import Benefit, FAQItem, GalleryItem, OrderStep, Review, SiteConfiguration


DEFAULT_KEYWORDS = (
    "\u043c\u0435\u0440\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0435 "
    "\u0430\u043a\u0432\u0430\u0440\u0438\u0443\u043c\u043d\u044b\u0435 "
    "\u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f, in vitro "
    "\u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f, \u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f "
    "\u0434\u043b\u044f \u0430\u043a\u0432\u0430\u0440\u0438\u0443\u043c\u0430, aquascape, "
    "Aquaklon, \u0430\u043a\u0432\u0430\u0440\u0438\u0443\u043c\u043d\u044b\u0435 "
    "\u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f \u041c\u043e\u0441\u043a\u0432\u0430"
)
DEFAULT_FAQ_EYEBROW = "FAQ"
DEFAULT_FAQ_TITLE = (
    "\u0427\u0430\u0441\u0442\u044b\u0435 \u0432\u043e\u043f\u0440\u043e\u0441\u044b "
    "\u043f\u0440\u043e \u043c\u0435\u0440\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0435 "
    "\u0430\u043a\u0432\u0430\u0440\u0438\u0443\u043c\u043d\u044b\u0435 \u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f"
)
DEFAULT_FAQ_LEAD = (
    "\u0421\u043e\u0431\u0440\u0430\u043b\u0438 \u043e\u0442\u0432\u0435\u0442\u044b \u043d\u0430 "
    "\u0432\u043e\u043f\u0440\u043e\u0441\u044b, \u043a\u043e\u0442\u043e\u0440\u044b\u0435 "
    "\u0447\u0430\u0449\u0435 \u0432\u0441\u0435\u0433\u043e \u0432\u043e\u0437\u043d\u0438\u043a\u0430\u044e\u0442 "
    "\u043f\u0435\u0440\u0435\u0434 \u0437\u0430\u043f\u0443\u0441\u043a\u043e\u043c \u0438\u043b\u0438 "
    "\u043f\u0435\u0440\u0435\u0441\u0430\u0434\u043a\u043e\u0439 \u0430\u043a\u0432\u0430\u0440\u0438\u0443\u043c\u0430."
)


@dataclass(frozen=True)
class FaqEntry:
    question: str
    answer: str


DEFAULT_FAQ_ITEMS = (
    FaqEntry(
        question=(
            "\u041a\u0430\u043a \u0432\u044b\u0431\u0440\u0430\u0442\u044c "
            "\u043c\u0435\u0440\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0435 "
            "\u0430\u043a\u0432\u0430\u0440\u0438\u0443\u043c\u043d\u044b\u0435 "
            "\u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f \u0434\u043b\u044f "
            "\u043d\u043e\u0432\u043e\u0433\u043e \u0430\u043a\u0432\u0430\u0440\u0438\u0443\u043c\u0430?"
        ),
        answer=(
            "\u041d\u0430\u0447\u0438\u043d\u0430\u0442\u044c \u0441\u0442\u043e\u0438\u0442 "
            "\u0441 \u0443\u0447\u0435\u0442\u0430 \u043e\u0431\u044a\u0435\u043c\u0430 "
            "\u0430\u043a\u0432\u0430\u0440\u0438\u0443\u043c\u0430, \u0441\u0432\u0435\u0442\u0430, "
            "\u043f\u043e\u0434\u0430\u0447\u0438 CO2 \u0438 \u0437\u0430\u0434\u0430\u0447\u0438 "
            "\u043a\u043e\u043c\u043f\u043e\u0437\u0438\u0446\u0438\u0438. \u0414\u043b\u044f "
            "\u043f\u0435\u0440\u0432\u043e\u0433\u043e \u0437\u0430\u043f\u0443\u0441\u043a\u0430 "
            "\u0447\u0430\u0441\u0442\u043e \u0432\u044b\u0431\u0438\u0440\u0430\u044e\u0442 "
            "\u043d\u0435\u043f\u0440\u0438\u0445\u043e\u0442\u043b\u0438\u0432\u044b\u0435 "
            "\u043f\u043e\u0447\u0432\u043e\u043f\u043e\u043a\u0440\u043e\u0432\u043d\u044b\u0435, "
            "\u0440\u043e\u0437\u0435\u0442\u043e\u0447\u043d\u044b\u0435 \u0438 "
            "\u0441\u0442\u0435\u0431\u0435\u043b\u044c\u043d\u044b\u0435 \u0432\u0438\u0434\u044b, "
            "\u043a\u043e\u0442\u043e\u0440\u044b\u0435 \u043b\u0435\u0433\u043a\u043e "
            "\u0430\u0434\u0430\u043f\u0442\u0438\u0440\u0443\u044e\u0442\u0441\u044f."
        ),
    ),
    FaqEntry(
        question=(
            "\u0427\u0435\u043c in vitro \u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f "
            "\u043e\u0442\u043b\u0438\u0447\u0430\u044e\u0442\u0441\u044f \u043e\u0442 "
            "\u043e\u0431\u044b\u0447\u043d\u044b\u0445 \u0430\u043a\u0432\u0430\u0440\u0438\u0443\u043c\u043d\u044b\u0445 "
            "\u0440\u0430\u0441\u0442\u0435\u043d\u0438\u0439?"
        ),
        answer=(
            "\u041c\u0435\u0440\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0435 "
            "\u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f \u0432\u044b\u0440\u0430\u0449\u0438\u0432\u0430\u044e\u0442\u0441\u044f "
            "\u0432 \u0441\u0442\u0435\u0440\u0438\u043b\u044c\u043d\u043e\u0439 \u0441\u0440\u0435\u0434\u0435, "
            "\u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u0432 \u0431\u0430\u043d\u043e\u0447\u043a\u0435 "
            "\u043d\u0435\u0442 \u0443\u043b\u0438\u0442\u043e\u043a, \u0432\u043e\u0434\u043e\u0440\u043e\u0441\u043b\u0435\u0439 "
            "\u0438 \u043d\u0435\u0436\u0435\u043b\u0430\u0442\u0435\u043b\u044c\u043d\u044b\u0445 "
            "\u043f\u0440\u0438\u043c\u0435\u0441\u0435\u0439. \u042d\u0442\u043e \u0443\u0434\u043e\u0431\u043d\u043e "
            "\u0434\u043b\u044f \u0447\u0438\u0441\u0442\u043e\u0433\u043e \u0441\u0442\u0430\u0440\u0442\u0430, "
            "\u0442\u043e\u0447\u043d\u043e\u0439 \u043f\u043e\u0441\u0430\u0434\u043a\u0438 \u0438 "
            "\u043f\u043b\u043e\u0442\u043d\u044b\u0445 \u0430\u043a\u0432\u0430\u0441\u043a\u0435\u0439\u043f-\u043a\u043e\u043c\u043f\u043e\u0437\u0438\u0446\u0438\u0439."
        ),
    ),
    FaqEntry(
        question=(
            "\u041c\u043e\u0436\u043d\u043e \u043b\u0438 \u0432\u044b\u0441\u0430\u0436\u0438\u0432\u0430\u0442\u044c "
            "\u043c\u0435\u0440\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0435 "
            "\u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f \u0431\u0435\u0437 CO2?"
        ),
        answer=(
            "\u0414\u0430, \u0447\u0430\u0441\u0442\u044c \u0432\u0438\u0434\u043e\u0432 "
            "\u043c\u043e\u0436\u0435\u0442 \u0440\u0430\u0441\u0442\u0438 \u0438 \u0431\u0435\u0437 "
            "\u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0439 "
            "\u043f\u043e\u0434\u0430\u0447\u0438 CO2, \u0435\u0441\u043b\u0438 "
            "\u043f\u043e\u0434\u043e\u0431\u0440\u0430\u043d\u044b \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0439 "
            "\u0441\u0432\u0435\u0442, \u043f\u0438\u0442\u0430\u0442\u0435\u043b\u044c\u043d\u044b\u0439 "
            "\u0433\u0440\u0443\u043d\u0442 \u0438 \u0441\u0442\u0430\u0431\u0438\u043b\u044c\u043d\u044b\u0439 "
            "\u0443\u0445\u043e\u0434. \u0414\u043b\u044f \u0431\u044b\u0441\u0442\u0440\u043e\u0433\u043e "
            "\u043f\u043e\u043a\u0440\u043e\u0432\u0430 \u0438 \u0441\u043b\u043e\u0436\u043d\u044b\u0445 "
            "\u043a\u043e\u043c\u043f\u043e\u0437\u0438\u0446\u0438\u0439 CO2 \u0432\u0441\u0451 \u0436\u0435 "
            "\u0434\u0430\u0451\u0442 \u0431\u043e\u043b\u0435\u0435 \u043f\u0440\u0435\u0434\u0441\u043a\u0430\u0437\u0443\u0435\u043c\u044b\u0439 "
            "\u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442."
        ),
    ),
    FaqEntry(
        question=(
            "\u041a\u0430\u043a \u0437\u0430\u043a\u0430\u0437\u0430\u0442\u044c "
            "\u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f Aquaklon \u0432 "
            "\u041c\u043e\u0441\u043a\u0432\u0435 \u0438 \u0443\u0442\u043e\u0447\u043d\u0438\u0442\u044c "
            "\u043d\u0430\u043b\u0438\u0447\u0438\u0435?"
        ),
        answer=(
            "\u0411\u044b\u0441\u0442\u0440\u0435\u0435 \u0432\u0441\u0435\u0433\u043e "
            "\u043d\u0430\u043f\u0438\u0441\u0430\u0442\u044c \u0438\u043b\u0438 "
            "\u043f\u043e\u0437\u0432\u043e\u043d\u0438\u0442\u044c \u043f\u043e "
            "\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u0430\u043c \u043d\u0430 "
            "\u0441\u0430\u0439\u0442\u0435: \u043c\u043e\u0436\u043d\u043e "
            "\u0443\u0442\u043e\u0447\u043d\u0438\u0442\u044c \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u0435 "
            "\u043d\u0430\u043b\u0438\u0447\u0438\u0435, \u043f\u043e\u0434\u043e\u0431\u0440\u0430\u0442\u044c "
            "\u0440\u0430\u0441\u0442\u0435\u043d\u0438\u044f \u043f\u043e\u0434 "
            "\u043e\u0431\u044a\u0435\u043c \u0430\u043a\u0432\u0430\u0440\u0438\u0443\u043c\u0430 \u0438 "
            "\u043f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0440\u0435\u043a\u043e\u043c\u0435\u043d\u0434\u0430\u0446\u0438\u0438 "
            "\u043f\u043e \u043f\u043e\u0441\u0430\u0434\u043a\u0435."
        ),
    ),
)


def get_site_configuration():
    config = SiteConfiguration.objects.first()
    if config is None:
        config = SiteConfiguration.objects.create()
    return config


def get_absolute_url(request, path_or_url):
    if not path_or_url:
        return ""
    return request.build_absolute_uri(path_or_url)


def get_canonical_url(request, config):
    if config.canonical_url:
        return config.canonical_url
    return request.build_absolute_uri(reverse("catalog:home"))


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


def get_faq_items():
    faq_items = list(FAQItem.objects.filter(is_published=True))
    if faq_items:
        return faq_items
    return list(DEFAULT_FAQ_ITEMS)


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
        {
            "loc": get_absolute_url(request, config.about_image_url),
            "caption": config.about_title,
            "title": config.about_panel_title,
        },
        {
            "loc": get_absolute_url(request, config.plants_image_url),
            "caption": config.plants_title,
            "title": config.plants_panel_title,
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


def build_structured_data(request, config, canonical_url, page_last_modified, reviews, faq_items):
    organization_id = f"{canonical_url}#organization"
    website_id = f"{canonical_url}#website"
    webpage_id = f"{canonical_url}#webpage"
    logo_url = get_absolute_url(request, config.logo_url)
    social_image_url = get_absolute_url(request, config.social_image_url)
    review_items = list(reviews[:3])
    same_as = [url for url in (config.whatsapp_url, config.max_url) if url]

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

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
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

    return [
        json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
        for schema in (organization_schema, website_schema, webpage_schema, faq_schema)
    ]


def build_home_context(request):
    config = get_site_configuration()
    benefits = list(Benefit.objects.filter(is_published=True))
    gallery_items = list(GalleryItem.objects.filter(is_published=True))
    order_steps = list(OrderStep.objects.filter(is_published=True))
    reviews = list(Review.objects.filter(is_published=True))
    faq_items = get_faq_items()
    canonical_url = get_canonical_url(request, config)
    page_last_modified = get_site_last_modified()

    seo_context = {
        "canonical_url": canonical_url,
        "keywords": config.seo_keywords or DEFAULT_KEYWORDS,
        "meta_robots": config.meta_robots,
        "og_image_url": get_absolute_url(request, config.social_image_url),
        "og_image_alt": config.social_image_alt or config.site_title,
        "hero_image_url": get_absolute_url(request, config.hero_image_url),
        "logo_url": get_absolute_url(request, config.logo_url),
        "page_last_modified": page_last_modified,
        "sitemap_url": request.build_absolute_uri(reverse("catalog:sitemap")),
        "structured_data": build_structured_data(
            request=request,
            config=config,
            canonical_url=canonical_url,
            page_last_modified=page_last_modified,
            reviews=reviews,
            faq_items=faq_items,
        ),
    }

    return {
        "config": config,
        "benefits": benefits,
        "gallery_items": gallery_items,
        "order_steps": order_steps,
        "reviews": reviews,
        "faq_items": faq_items,
        "faq_eyebrow": DEFAULT_FAQ_EYEBROW,
        "faq_title": DEFAULT_FAQ_TITLE,
        "faq_lead": DEFAULT_FAQ_LEAD,
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
            "sitemap_url": request.build_absolute_uri(reverse("catalog:sitemap")),
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
