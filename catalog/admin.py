from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from .models import Benefit, FAQItem, GalleryItem, OrderStep, Review, SiteConfiguration


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


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    readonly_fields = (
        "logo_preview",
        "social_image_preview",
        "hero_image_preview",
        "about_image_preview",
        "plants_image_preview",
    )
    fieldsets = (
        (
            "Brand and SEO",
            {
                "fields": (
                    "brand_name",
                    "brand_caption",
                    "site_title",
                    "meta_description",
                    "canonical_url",
                    "seo_keywords",
                    "meta_robots",
                    "google_site_verification",
                    "yandex_verification",
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
            "Navigation",
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
            "Hero",
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
            "About",
            {
                "fields": (
                    "about_eyebrow",
                    "about_title",
                    "about_body_1",
                    "about_body_2",
                    "about_panel_title",
                    "about_panel_text",
                    "about_image",
                    "about_image_preview",
                )
            },
        ),
        (
            "Advantages Section",
            {
                "description": "Cards in this section are managed separately in the Benefits list.",
                "fields": (
                    "advantages_eyebrow",
                    "advantages_title",
                    "advantages_text",
                )
            },
        ),
        (
            "Plants",
            {
                "fields": (
                    "plants_eyebrow",
                    "plants_title",
                    "plants_text",
                    "plants_panel_title",
                    "plants_panel_text",
                    "plants_image",
                    "plants_image_preview",
                )
            },
        ),
        (
            "Gallery, Reviews and Contacts",
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
                    "whatsapp_url",
                    "max_url",
                )
            },
        ),
    )

    def changelist_view(self, request, extra_context=None):
        config, _created = SiteConfiguration.objects.get_or_create(pk=1)
        return HttpResponseRedirect(reverse("admin:catalog_siteconfiguration_change", args=[config.pk]))

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def logo_preview(self, obj):
        return render_preview(obj.logo_url, obj.brand_name)

    logo_preview.short_description = "Logo preview"

    def hero_image_preview(self, obj):
        return render_preview(obj.hero_image_url, obj.hero_title, size=180)

    hero_image_preview.short_description = "Hero preview"

    def social_image_preview(self, obj):
        return render_preview(obj.social_image_url, obj.social_image_alt or obj.site_title, size=180)

    social_image_preview.short_description = "Social preview"

    def about_image_preview(self, obj):
        return render_preview(obj.about_image_url, obj.about_title, size=180)

    about_image_preview.short_description = "About preview"

    def plants_image_preview(self, obj):
        return render_preview(obj.plants_image_url, obj.plants_title, size=180)

    plants_image_preview.short_description = "Plants preview"


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
            "Content",
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
            "Publishing",
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

    image_preview.short_description = "Photo"

    def image_preview_large(self, obj):
        return render_preview(obj.display_image_url, obj.title, size=220)

    image_preview_large.short_description = "Preview"


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


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question", "sort_order", "is_published")
    list_editable = ("sort_order", "is_published")
    ordering = ("sort_order", "id")
    fields = ("question", "answer", "sort_order", "is_published")


UserModel = get_user_model()
if UserModel in admin.site._registry:
    admin.site.unregister(UserModel)
if Group in admin.site._registry:
    admin.site.unregister(Group)

admin.site.site_header = "Aquaklon admin"
admin.site.site_title = "Aquaklon admin"
admin.site.index_title = "Site content management"
admin.site.site_url = "/"
