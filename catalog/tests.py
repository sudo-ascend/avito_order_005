from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from .models import Benefit, FAQItem, GalleryItem, OrderStep, Review, SiteConfiguration


class HomePageTests(TestCase):
    def test_home_page_renders_dynamic_content(self):
        Benefit.objects.create(icon="shield", title="Clean start", text="Sterile culture", sort_order=1)
        Benefit.objects.create(icon="cup", title="Compact format", text="Easy to place", sort_order=2)
        OrderStep.objects.create(title="Step one", text="Choose plants", sort_order=1)
        OrderStep.objects.create(title="Step two", text="Confirm availability", sort_order=2)

        response = self.client.get(reverse("catalog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aquaklon")
        self.assertContains(response, "Clean start")
        self.assertContains(response, "Compact format")
        self.assertContains(response, "Step one")
        self.assertContains(response, "Step two")

    def test_home_page_contains_seo_metadata_and_schema(self):
        SiteConfiguration.objects.create(
            canonical_url="https://aquaklon.example/",
            seo_keywords="aquarium plants, in vitro plants",
            google_site_verification="google-code",
            yandex_verification="yandex-code",
        )
        FAQItem.objects.create(
            question="How to choose in vitro plants?",
            answer="Match them to light, CO2 and aquarium size.",
            sort_order=1,
        )

        response = self.client.get(reverse("catalog:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rel="canonical" href="https://aquaklon.example/"', html=False)
        self.assertContains(response, 'name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"', html=False)
        self.assertContains(response, 'property="og:type" content="website"', html=False)
        self.assertContains(response, 'name="twitter:card" content="summary_large_image"', html=False)
        self.assertContains(response, 'name="google-site-verification" content="google-code"', html=False)
        self.assertContains(response, 'name="yandex-verification" content="yandex-code"', html=False)
        self.assertContains(response, "application/ld+json")
        self.assertContains(response, "How to choose in vitro plants?")
        self.assertEqual(
            response.headers["X-Robots-Tag"],
            "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1",
        )
        self.assertIn("Last-Modified", response.headers)

    def test_robots_and_sitemap_endpoints_render(self):
        GalleryItem.objects.create(
            title="Showcase",
            text="Gallery item for sitemap",
            image_path="gallery-aquascape-1.webp",
            sort_order=1,
        )

        robots_response = self.client.get(reverse("catalog:robots"))
        sitemap_response = self.client.get(reverse("catalog:sitemap"))

        self.assertEqual(robots_response.status_code, 200)
        self.assertContains(robots_response, "Disallow: /admin/")
        self.assertContains(robots_response, "Sitemap: http://testserver/sitemap.xml")

        self.assertEqual(sitemap_response.status_code, 200)
        self.assertContains(sitemap_response, "<loc>http://testserver/</loc>", html=False)
        self.assertContains(sitemap_response, "<image:loc>http://testserver/static/gallery-aquascape-1.webp</image:loc>", html=False)


class AdminContentModeTests(TestCase):
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
        self.assertIn(Review, registry)
        self.assertIn(FAQItem, registry)
        self.assertNotIn(get_user_model(), registry)
        self.assertNotIn(Group, registry)
