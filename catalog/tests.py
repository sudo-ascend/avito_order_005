import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .models import Benefit, GalleryItem, OrderStep, PlantProduct, Review, SiteConfiguration


@override_settings(SITE_URL="http://testserver")
class HomePageTests(TestCase):
    def test_home_page_renders_dynamic_content(self):
        Benefit.objects.create(icon="shield", title="Clean start", text="Sterile culture", sort_order=1)
        Benefit.objects.create(icon="cup", title="Compact format", text="Easy to place", sort_order=2)
        OrderStep.objects.create(title="Step one", text="Choose plants", sort_order=1)
        OrderStep.objects.create(title="Step two", text="Confirm availability", sort_order=2)
        PlantProduct.objects.create(
            slug="anubias-barteri",
            title="Anubias barteri",
            latin_name="Anubias barteri var. nana",
            description="Hardy foreground plant",
            image_path="plants/plants_4.webp",
            image_alt="Anubias barteri",
            sort_order=1,
        )

        response = self.client.get(reverse("catalog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aquaklon")
        self.assertContains(response, "Clean start")
        self.assertContains(response, "Compact format")
        self.assertContains(response, "Step one")
        self.assertContains(response, "Step two")
        self.assertContains(response, "Anubias barteri")
        self.assertContains(response, "Hardy foreground plant")
        self.assertContains(response, 'src="/static/plants/plants_4.webp"', html=False)

    def test_home_page_shows_delivery_terms_download_button_when_file_is_configured(self):
        config = SiteConfiguration.objects.first() or SiteConfiguration()
        config.delivery_terms_file = "site/delivery-terms/order-delivery-terms.pdf"
        config.delivery_terms_file_original_name = "delivery-terms.pdf"
        config.save()

        response = self.client.get(reverse("catalog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Условия заказа и доставки")
        self.assertContains(response, 'href="/media/site/delivery-terms/order-delivery-terms.pdf"', html=False)
        self.assertContains(response, 'download="delivery-terms.pdf"', html=False)

    def test_home_page_shows_delivery_terms_download_button_with_default_path(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Условия заказа и доставки")
        self.assertContains(response, 'href="media/site/delivery-terms/order-delivery-terms.pdf"', html=False)
        self.assertContains(response, 'download="order-delivery-terms.pdf"', html=False)

    def test_home_page_contains_seo_metadata_and_schema(self):
        config = SiteConfiguration.objects.first() or SiteConfiguration()
        config.telegram_url = "https://t.me/microklon"
        config.save()
        response = self.client.get(reverse("catalog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rel="canonical" href="http://testserver/"', html=False)
        self.assertContains(response, 'name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"', html=False)
        self.assertContains(response, 'property="og:type" content="website"', html=False)
        self.assertContains(response, 'name="twitter:card" content="summary_large_image"', html=False)
        self.assertNotContains(response, "google-site-verification")
        self.assertNotContains(response, "yandex-verification")
        self.assertContains(response, "application/ld+json")
        self.assertContains(response, 'href="https://t.me/microklon"', html=False)
        self.assertContains(response, "Написать в Telegram")
        self.assertContains(response, "https://t.me/microklon")
        self.assertEqual(
            response.headers["X-Robots-Tag"],
            "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1",
        )
        self.assertIn("Last-Modified", response.headers)

    def test_robots_and_sitemap_endpoints_render(self):
        GalleryItem.objects.create(
            title="Showcase",
            text="Gallery item for sitemap",
            image_path="gallery_1.webp",
            sort_order=1,
        )
        PlantProduct.objects.create(
            slug="test-sitemap-plant",
            title="Test sitemap plant",
            description="Plant item for sitemap",
            image_path="plants/plants_2.webp",
            image_alt="Test sitemap plant",
            sort_order=1,
        )

        robots_response = self.client.get(reverse("catalog:robots"))
        sitemap_response = self.client.get(reverse("catalog:sitemap"))

        self.assertEqual(robots_response.status_code, 200)
        self.assertContains(robots_response, "Disallow: /admin/")
        self.assertContains(robots_response, "Sitemap: http://testserver/sitemap.xml")

        self.assertEqual(sitemap_response.status_code, 200)
        self.assertContains(sitemap_response, "<loc>http://testserver/</loc>", html=False)
        self.assertContains(sitemap_response, "<image:loc>http://testserver/static/gallery_1.webp</image:loc>", html=False)
        self.assertContains(
            sitemap_response,
            "<image:loc>http://testserver/static/plants/plants_2.webp</image:loc>",
            html=False,
        )

    def test_yandex_verification_file_is_available(self):
        response = self.client.get(reverse("catalog:yandex_verification"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Verification: 4d153c26552f0309")

    def test_error_preview_pages_are_available(self):
        preview_routes = [
            ("catalog:error_400_preview", 400),
            ("catalog:error_403_preview", 403),
            ("catalog:error_404_preview", 404),
            ("catalog:error_500_preview", 500),
        ]

        for route_name, expected_status in preview_routes:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, expected_status)
                self.assertEqual(response.headers["X-Robots-Tag"], "noindex, nofollow, noarchive")


@override_settings()
class AdminContentModeTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temp_media_dir = tempfile.mkdtemp()
        super().setUpClass()
        cls.enterClassContext(override_settings(MEDIA_ROOT=cls._temp_media_dir))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(cls._temp_media_dir, ignore_errors=True)

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pass12345",
        )

    def test_singleton_configuration_redirects_to_change_form(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin:catalog_siteconfiguration_changelist"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("admin:catalog_siteconfiguration_change", args=[1]), fetch_redirect_response=False)
        self.assertTrue(SiteConfiguration.objects.filter(pk=1).exists())

    def test_only_content_models_are_registered_in_admin(self):
        registry = admin.site._registry

        self.assertIn(SiteConfiguration, registry)
        self.assertIn(Benefit, registry)
        self.assertIn(GalleryItem, registry)
        self.assertIn(OrderStep, registry)
        self.assertIn(PlantProduct, registry)
        self.assertIn(Review, registry)
        self.assertNotIn(get_user_model(), registry)
        self.assertNotIn(Group, registry)

    def test_admin_index_contains_price_file_controls(self):
        config = SiteConfiguration.objects.first() or SiteConfiguration()
        config.price_file_original_name = "old-price.xlsx"
        config.price_file = "site/prices/price-list.xlsx"
        config.delivery_terms_file_original_name = "delivery-terms.pdf"
        config.delivery_terms_file = "site/delivery-terms/order-delivery-terms.pdf"
        config.save()
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="price_file"', html=False)
        self.assertContains(response, "old-price.xlsx")
        self.assertContains(response, 'name="delivery_terms_file"', html=False)
        self.assertContains(response, "delivery-terms.pdf")
        self.assertContains(response, "Тексты и изображения")
        self.assertContains(response, "Преимущества")
        self.assertContains(response, "Этапы заказа")

    def test_admin_index_contains_plant_catalog_section(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/admin/catalog/plantproduct/", html=False)

    def test_site_configuration_admin_uses_russian_labels(self):
        SiteConfiguration.objects.get_or_create(pk=1)
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin:catalog_siteconfiguration_change", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Бренд и SEO")
        self.assertContains(response, "Первый экран")
        self.assertContains(response, "Электронная почта")
        self.assertContains(response, "Превью логотипа")

    def test_benefit_icon_choices_are_extended(self):
        icon_values = {value for value, _label in Benefit.ICON_CHOICES}

        self.assertGreaterEqual(len(icon_values), 12)
        self.assertTrue({"leaf", "drop", "sun", "star", "layers", "heart", "spark", "waves"}.issubset(icon_values))

    def test_admin_can_upload_new_price_file_from_dashboard(self):
        self.client.force_login(self.user)
        upload = SimpleUploadedFile(
            "new-prices.xlsx",
            b"updated price content",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response = self.client.post(
            reverse("admin:catalog_update_price_file"),
            {"price_file": upload},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        config = SiteConfiguration.objects.get(pk=1)
        self.assertEqual(config.price_file_original_name, "new-prices.xlsx")
        self.assertEqual(config.price_file.name, "site/prices/price-list.xlsx")
        self.assertTrue((Path(settings.MEDIA_ROOT) / "site" / "prices" / "price-list.xlsx").exists())
        self.assertContains(response, "new-prices.xlsx")

    def test_admin_can_upload_delivery_terms_file_from_dashboard(self):
        self.client.force_login(self.user)
        upload = SimpleUploadedFile(
            "delivery-terms.pdf",
            b"delivery terms content",
            content_type="application/pdf",
        )

        response = self.client.post(
            reverse("admin:catalog_update_delivery_terms_file"),
            {"delivery_terms_file": upload},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        config = SiteConfiguration.objects.get(pk=1)
        self.assertEqual(config.delivery_terms_file_original_name, "delivery-terms.pdf")
        self.assertEqual(config.delivery_terms_file.name, "site/delivery-terms/order-delivery-terms.pdf")
        self.assertTrue((Path(settings.MEDIA_ROOT) / "site" / "delivery-terms" / "order-delivery-terms.pdf").exists())
        self.assertContains(response, "delivery-terms.pdf")
