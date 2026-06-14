from decimal import Decimal
from pathlib import Path

from django.core.files.storage import FileSystemStorage
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.templatetags.static import static


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name


def upload_price_file(_instance, filename):
    suffix = Path(filename).suffix.lower() or ".xlsx"
    return f"site/prices/price-list{suffix}"


class SiteConfiguration(SingletonModel):
    brand_name = models.CharField("Название бренда", max_length=120, default="Aquaklon")
    brand_caption = models.CharField("Подпись бренда", max_length=160, default="меристемные растения")
    site_title = models.CharField("Заголовок сайта", max_length=255, default="Aquaklon - меристемные аквариумные растения")
    meta_description = models.TextField(
        "Мета-описание",
        default="Меристемные аквариумные растения Aquaklon для акваскейпа, домашних и профессиональных аквариумов.",
    )
    meta_robots = models.CharField(
        "Директивы robots",
        max_length=160,
        default="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1",
    )
    social_image = models.ImageField("Изображение для соцсетей", upload_to="site/seo", blank=True, null=True)
    social_image_alt = models.CharField("Описание изображения для соцсетей", max_length=255, blank=True, default="")
    contact_phone = models.CharField("Телефон для ссылок", max_length=32, default="+79266019274")
    contact_phone_display = models.CharField("Телефон для показа", max_length=32, default="8-926-601-92-74")
    contact_email = models.EmailField("Электронная почта", default="Aquaklon@yandex.ru")
    contact_city = models.CharField("Город", max_length=120, default="Москва")
    whatsapp_url = models.URLField("Ссылка WhatsApp", blank=True, default="https://wa.me/79266019274")
    max_url = models.URLField("Ссылка MAX", blank=True, default="https://web.max.ru/83411154")
    telegram_url = models.URLField("Ссылка Telegram", blank=True, default="https://t.me/microklon")

    nav_about_label = models.CharField("Пункт меню О нас", max_length=80, default="О нас")
    nav_advantages_label = models.CharField("Пункт меню Преимущества", max_length=80, default="Преимущества")
    nav_plants_label = models.CharField("Пункт меню Растения", max_length=80, default="Растения")
    nav_aquariums_label = models.CharField("Пункт меню Аквариумы", max_length=80, default="Аквариумы")
    nav_reviews_label = models.CharField("Пункт меню Отзывы", max_length=80, default="Отзывы")
    nav_contacts_label = models.CharField("Пункт меню Контакты", max_length=80, default="Контакты")

    header_contact_button_text = models.CharField("Текст кнопки в шапке", max_length=80, default="Связаться")
    hero_eyebrow = models.CharField(
        "Первый экран: надзаголовок",
        max_length=255,
        default="Работаем в г. Москва · культура in vitro · акваскейп",
    )
    hero_title = models.TextField(
        "Первый экран: заголовок",
        default="Меристемные аквариумные растения для красивого и здорового аквариума",
    )
    hero_lead = models.TextField(
        "Первый экран: описание",
        default="Aquaklon выращивает качественные аквариумные растения для акваскейпа, домашних и профессиональных аквариумов.",
    )
    hero_primary_button_text = models.CharField("Первый экран: кнопка 1", max_length=80, default="Узнать наличие")
    hero_secondary_button_text = models.CharField("Первый экран: кнопка 2", max_length=80, default="Посмотреть растения")
    hero_feature_1 = models.CharField("Первый экран: преимущество 1", max_length=120, default="Меристемное выращивание")
    hero_feature_2 = models.CharField("Первый экран: преимущество 2", max_length=120, default="Чистая культура")
    hero_feature_3 = models.CharField("Первый экран: преимущество 3", max_length=120, default="Подходит для акваскейпа")
    hero_feature_4 = models.CharField("Первый экран: преимущество 4", max_length=120, default="Работаем в г. Москва")

    about_eyebrow = models.CharField("О нас надзаголовок", max_length=120, default="О компании")
    about_title = models.TextField("О нас заголовок", default="Чистые растения для уверенного запуска аквариума")
    about_body_1 = models.TextField(
        "О нас абзац 1",
        default="Aquaklon занимается выращиванием и продажей меристемных аквариумных растений. Такие растения развиваются в стерильных условиях, поэтому покупатель получает чистый и удобный посадочный материал.",
    )
    about_body_2 = models.TextField(
        "О нас абзац 2",
        default="Формат in vitro хорошо подходит для новых запусков, плотных растительных композиций и аккуратного акваскейпа.",
    )
    about_panel_title = models.CharField("Карточка О нас заголовок", max_length=120, default="Стерильная культура")
    about_panel_text = models.CharField(
        "Карточка О нас текст",
        max_length=255,
        default="Чистый старт для посадки, оформления и доращивания.",
    )

    logo = models.ImageField("Логотип сайта", upload_to="site/branding", blank=True, null=True)
    hero_image = models.ImageField("Изображение первого экрана", upload_to="site/sections", blank=True, null=True)

    advantages_eyebrow = models.CharField("Преимущества надзаголовок", max_length=120, default="Почему меристема")
    advantages_title = models.TextField("Преимущества заголовок", default="Растения, с которыми удобно работать")
    advantages_text = models.TextField(
        "Преимущества описание",
        default="Меристемные растения ценят за чистоту, компактность и предсказуемую посадку.",
    )
    plants_eyebrow = models.CharField("Растения надзаголовок", max_length=120, default="Каталог растений")
    plants_title = models.TextField("Растения заголовок", default="Популярные виды для аквариума и акваскейпа")
    aquariums_eyebrow = models.CharField("Галерея надзаголовок", max_length=120, default="Живые композиции")
    aquariums_title = models.TextField("Галерея заголовок", default="Аквариумы, созданные из наших растений")
    aquariums_text = models.TextField(
        "Галерея описание",
        default="Примеры композиций, где растения подчеркивают объем, глубину и живую фактуру аквариума.",
    )

    order_eyebrow = models.CharField("Заказ надзаголовок", max_length=120, default="Как заказать")
    order_title = models.TextField("Заказ заголовок", default="Простой путь от выбора до посадки")
    reviews_eyebrow = models.CharField("Отзывы надзаголовок", max_length=120, default="Отзывы клиентов")
    reviews_title = models.TextField(
        "Отзывы заголовок",
        default="Растения хорошо доезжают, приживаются и смотрятся естественно",
    )
    reviews_rating = models.DecimalField(
        "Рейтинг",
        max_digits=3,
        decimal_places=1,
        default=Decimal("4.8"),
        validators=[MinValueValidator(Decimal("0.0")), MaxValueValidator(Decimal("5.0"))],
    )

    contacts_eyebrow = models.CharField("Контакты надзаголовок", max_length=120, default="Контакты")
    contacts_title = models.TextField("Контакты заголовок", default="Уточните наличие растений Aquaklon")
    contacts_text = models.TextField(
        "Контакты описание",
        default="Подскажем по ассортименту, посадке и выбору растений под ваш аквариум.",
    )
    contacts_call_button_text = models.CharField("Кнопка Позвонить", max_length=80, default="Позвонить")
    contacts_email_button_text = models.CharField("Кнопка Написать на почту", max_length=80, default="Написать на почту")
    contacts_whatsapp_button_text = models.CharField("Кнопка WhatsApp", max_length=80, default="Написать в WhatsApp")
    contacts_max_button_text = models.CharField("Кнопка MAX", max_length=80, default="Написать в MAX")
    contacts_telegram_button_text = models.CharField("Кнопка Telegram", max_length=80, default="Написать в Telegram")
    price_file = models.FileField(
        "Файл с ценами",
        upload_to=upload_price_file,
        storage=OverwriteStorage(),
        blank=True,
        null=True,
    )
    price_file_original_name = models.CharField("Имя файла с ценами", max_length=255, blank=True, default="")

    footer_text = models.CharField("Текст в подвале", max_length=255, default="Москва · 8-926-601-92-74 · Aquaklon@yandex.ru")

    class Meta:
        verbose_name = "Конфигурация сайта"
        verbose_name_plural = "Конфигурация сайта"

    def __str__(self):
        return "Конфигурация сайта"

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        return static("favicon.ico")

    @property
    def hero_image_url(self):
        if self.hero_image:
            return self.hero_image.url
        return static("hero/hero_1.webp")

    @property
    def social_image_url(self):
        if self.social_image:
            return self.social_image.url
        return static("hero/hero_1.webp")

    @property
    def price_file_url(self):
        if self.price_file:
            return self.price_file.url
        return ""

    @property
    def price_file_name(self):
        if self.price_file_original_name:
            return self.price_file_original_name
        if self.price_file:
            return Path(self.price_file.name).name
        return ""


class OrderedModel(models.Model):
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("Показывать на сайте", default=True)

    class Meta:
        abstract = True
        ordering = ("sort_order", "id")


class Benefit(OrderedModel):
    ICON_CHOICES = [
        ("shield", "Щит"),
        ("cup", "Контейнер"),
        ("tweezers", "Пинцет"),
        ("sprout", "Росток"),
        ("grid", "Сетка"),
        ("scape", "Акваскейп"),
        ("leaf", "Лист"),
        ("drop", "Капля"),
        ("sun", "Свет"),
        ("star", "Звезда"),
        ("layers", "Слои"),
        ("heart", "Сердце"),
        ("spark", "Искра"),
        ("waves", "Волны"),
    ]

    icon = models.CharField("Иконка", max_length=32, choices=ICON_CHOICES, default="shield")
    title = models.CharField("Заголовок", max_length=160)
    text = models.TextField("Описание")

    class Meta(OrderedModel.Meta):
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    def __str__(self):
        return self.title


class GalleryItem(OrderedModel):
    title = models.CharField("Заголовок", max_length=160)
    text = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="site/gallery", blank=True, null=True)
    image_path = models.CharField("Путь к изображению", max_length=255, blank=True, default="")
    image_alt = models.CharField("Альтернативный текст", max_length=255, blank=True, default="")

    class Meta(OrderedModel.Meta):
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Галерея"

    def __str__(self):
        return self.title

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        if self.image_path:
            return static(self.image_path)
        return ""


class OrderStep(OrderedModel):
    title = models.CharField("Заголовок", max_length=160)
    text = models.TextField("Описание")

    class Meta(OrderedModel.Meta):
        verbose_name = "Этап заказа"
        verbose_name_plural = "Этапы заказа"

    def __str__(self):
        return self.title


class Review(OrderedModel):
    name = models.CharField("Имя", max_length=120)
    rating = models.PositiveSmallIntegerField(
        "Рейтинг",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    text = models.TextField("Отзыв")

    class Meta(OrderedModel.Meta):
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.name
