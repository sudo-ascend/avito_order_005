from django.contrib import admin
from django.utils.html import format_html

from .models import GalleryItem, PlantProduct, PriceUpload, Review


class OrderedAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order", "is_published")
    list_editable = ("sort_order", "is_published")
    ordering = ("sort_order", "id")


@admin.register(GalleryItem)
class GalleryItemAdmin(OrderedAdmin):
    list_display = ("title", "image_path", "sort_order", "is_published")


@admin.register(Review)
class ReviewAdmin(OrderedAdmin):
    list_display = ("name", "rating", "sort_order", "is_published")
    list_editable = ("rating", "sort_order", "is_published")


@admin.register(PlantProduct)
class PlantProductAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "variety_name", "article", "container_type", "stock", "price", "is_published", "updated_at")
    list_filter = ("is_published", "container_type", "location")
    list_editable = ("is_published",)
    search_fields = ("variety_name", "latin_name", "article", "description", "location")
    ordering = ("variety_name", "article")
    readonly_fields = ("image_preview_large", "created_at", "updated_at")
    fieldsets = (
        (
            "РљР°СЂС‚РѕС‡РєР° С‚РѕРІР°СЂР° Рё С„РѕС‚Рѕ",
            {
                "fields": (
                    "variety_name",
                    "latin_name",
                    "article",
                    "description",
                    "image",
                    "image_preview_large",
                    "image_path",
                )
            },
        ),
        (
            "РџСЂР°Р№СЃ Рё РЅР°Р»РёС‡РёРµ",
            {
                "fields": (
                    "location",
                    "container_type",
                    "order_multiple",
                    "stock",
                    "price",
                    "discount_new",
                    "discount_legacy",
                    "discount_logo",
                    "order_note",
                )
            },
        ),
        (
            "РџСѓР±Р»РёРєР°С†РёСЏ Рё СЃР»СѓР¶РµР±РЅС‹Рµ РїРѕР»СЏ",
            {
                "fields": (
                    "is_published",
                    "source_row",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def image_preview(self, obj):
        if not obj.display_image_url:
            return "вЂ”"
        return format_html(
            '<img src="{}" alt="{}" style="width:44px;height:44px;object-fit:cover;border-radius:6px;" />',
            obj.display_image_url,
            obj.variety_name,
        )

    image_preview.short_description = "Р¤РѕС‚Рѕ"

    def image_preview_large(self, obj):
        if not obj.display_image_url:
            return "РР·РѕР±СЂР°Р¶РµРЅРёРµ РЅРµ Р·Р°РіСЂСѓР¶РµРЅРѕ"
        return format_html(
            '<img src="{}" alt="{}" style="max-width:220px;max-height:220px;object-fit:cover;border-radius:10px;border:1px solid #d8e5e0;" />',
            obj.display_image_url,
            obj.variety_name,
        )

    image_preview_large.short_description = "РџСЂРµРґРїСЂРѕСЃРјРѕС‚СЂ"


@admin.register(PriceUpload)
class PriceUploadAdmin(admin.ModelAdmin):
    list_display = ("original_filename", "uploaded_at", "uploaded_by", "update_requested", "is_merged", "row_count")
    list_filter = ("update_requested", "is_merged", "uploaded_at")
    readonly_fields = ("uploaded_at", "uploaded_by", "row_count", "change_summary", "parsed_payload")


admin.site.site_header = "Aquaklon admin"
admin.site.site_title = "Aquaklon admin"
admin.site.index_title = "РЈРїСЂР°РІР»РµРЅРёРµ СЃР°Р№С‚РѕРј"
admin.site.site_url = "/"
