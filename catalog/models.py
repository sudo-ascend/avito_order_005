from decimal import Decimal
import re

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.templatetags.static import static
from django.utils import timezone

User = get_user_model()
PRICE_UPLOAD_FILENAME_RE = re.compile(r"\d{2}_\d{2}_\d{4}-\d{2}-\d{2}-\d{2}\.xlsx")


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class SiteConfiguration(SingletonModel):
    brand_name = models.CharField("Название бренда", max_length=120, default="Aquaklon")
    brand_caption = models.CharField("Подпись бренда", max_length=160, default="меристемные растения")
    site_title = models.CharField("Title сайта", max_length=255, default="Aquaklon - меристемные аквариумные растения")
    meta_description = models.TextField(
        "Meta description",
        default="Меристемные аквариумные растения Aquaklon для акваскейпа, домашних и профессиональных аквариумов.",
    )
    canonical_url = models.URLField("Canonical URL", blank=True, default="")
    contact_phone = models.CharField("Телефон для ссылок", max_length=32, default="+79266019274")
    contact_phone_display = models.CharField("Телефон для показа", max_length=32, default="8-926-601-92-74")
    contact_email = models.EmailField("Email", default="Aquaklon@yandex.ru")
    contact_city = models.CharField("Город", max_length=120, default="Москва")
    whatsapp_url = models.URLField("Ссылка WhatsApp", blank=True, default="https://wa.me/79266019274")
    max_url = models.URLField("Ссылка MAX", blank=True, default="https://web.max.ru/83411154")

    nav_about_label = models.CharField("Пункт меню О нас", max_length=80, default="О нас")
    nav_advantages_label = models.CharField("Пункт меню Преимущества", max_length=80, default="Преимущества")
    nav_plants_label = models.CharField("Пункт меню Растения", max_length=80, default="Растения")
    nav_aquariums_label = models.CharField("Пункт меню Аквариумы", max_length=80, default="Аквариумы")
    nav_reviews_label = models.CharField("Пункт меню Отзывы", max_length=80, default="Отзывы")
    nav_contacts_label = models.CharField("Пункт меню Контакты", max_length=80, default="Контакты")

    header_contact_button_text = models.CharField("Текст кнопки в шапке", max_length=80, default="Связаться")
    hero_eyebrow = models.CharField("Hero надзаголовок", max_length=255, default="Работаем в г. Москва · культура in vitro · акваскейп")
    hero_title = models.TextField("Hero заголовок", default="Меристемные аквариумные растения для красивого и здорового аквариума")
    hero_lead = models.TextField(
        "Hero описание",
        default="Aquaklon выращивает качественные аквариумные растения для акваскейпа, домашних и профессиональных аквариумов.",
    )
    hero_primary_button_text = models.CharField("Hero кнопка 1", max_length=80, default="Узнать наличие")
    hero_secondary_button_text = models.CharField("Hero кнопка 2", max_length=80, default="Посмотреть растения")
    hero_feature_1 = models.CharField("Hero преимущество 1", max_length=120, default="Меристемное выращивание")
    hero_feature_2 = models.CharField("Hero преимущество 2", max_length=120, default="Чистая культура")
    hero_feature_3 = models.CharField("Hero преимущество 3", max_length=120, default="Подходит для акваскейпа")
    hero_feature_4 = models.CharField("Hero преимущество 4", max_length=120, default="Работаем в г. Москва")

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

    advantages_eyebrow = models.CharField("Преимущества надзаголовок", max_length=120, default="Почему меристема")
    advantages_title = models.TextField("Преимущества заголовок", default="Растения, с которыми удобно работать")
    advantages_text = models.TextField(
        "Преимущества описание",
        default="Меристемные растения ценят за чистоту, компактность и предсказуемую посадку.",
    )
    advantage_1_title = models.CharField("Преимущество 1 заголовок", max_length=160, default="Чистый посадочный материал")
    advantage_1_text = models.TextField("Преимущество 1 текст", default="Растения без лишней нагрузки и с предсказуемым стартом.")
    advantage_2_title = models.CharField("Преимущество 2 заголовок", max_length=160, default="Компактная форма")
    advantage_2_text = models.TextField("Преимущество 2 текст", default="Удобно высаживать и быстро формировать композиции.")
    advantage_3_title = models.CharField("Преимущество 3 заголовок", max_length=160, default="Подходит для акваскейпа")
    advantage_3_text = models.TextField("Преимущество 3 текст", default="Хорошо смотрится в природных и дизайнерских аквариумах.")
    advantage_4_title = models.CharField("Преимущество 4 заголовок", max_length=160, default="Работаем по Москве")
    advantage_4_text = models.TextField("Преимущество 4 текст", default="Помогаем с подбором и доставкой растений.")

    plants_eyebrow = models.CharField("Каталог надзаголовок", max_length=120, default="Каталог растений")
    plants_title = models.TextField("Каталог заголовок", default="Растения для аквариума и акваскейпа")
    product_button_text = models.CharField("Кнопка товара", max_length=80, default="Уточнить наличие")

    aquariums_eyebrow = models.CharField("Галерея надзаголовок", max_length=120, default="Живые композиции")
    aquariums_title = models.TextField("Галерея заголовок", default="Аквариумы, созданные из наших растений")
    aquariums_text = models.TextField(
        "Галерея описание",
        default="Примеры композиций, где растения подчеркивают объем, глубину и живую фактуру аквариума.",
    )

    order_eyebrow = models.CharField("Заказ надзаголовок", max_length=120, default="Как заказать")
    order_title = models.TextField("Заказ заголовок", default="Простой путь от выбора до посадки")
    order_step_1_title = models.CharField("Этап заказа 1 заголовок", max_length=160, default="Выберите растения")
    order_step_1_text = models.TextField("Этап заказа 1 текст", default="Соберите список растений, которые нужны для вашего аквариума.")
    order_step_2_title = models.CharField("Этап заказа 2 заголовок", max_length=160, default="Согласуйте наличие")
    order_step_2_text = models.TextField("Этап заказа 2 текст", default="Мы подтвердим актуальное наличие и подскажем варианты.")
    order_step_3_title = models.CharField("Этап заказа 3 заголовок", max_length=160, default="Оформите заказ")
    order_step_3_text = models.TextField("Этап заказа 3 текст", default="Напишите удобным способом и подтвердите состав заказа.")
    order_step_4_title = models.CharField("Этап заказа 4 заголовок", max_length=160, default="Получите и посадите")
    order_step_4_text = models.TextField("Этап заказа 4 текст", default="Заберите растения и высадите их в аквариум.")

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

    footer_text = models.CharField("Текст в подвале", max_length=255, default="Москва · 8-926-601-92-74 · Aquaklon@yandex.ru")
    price_notice = models.TextField(
        "Примечание для прайс-листа",
        blank=True,
        default="Уважаемые аквариумисты, следите за актуальностью прайс-листа перед оформлением заказа.",
    )
    price_catalog_title = models.CharField(
        "Заголовок прайс-листа",
        max_length=255,
        default="Наличие меристемных аквариумных растений",
    )

    class Meta:
        verbose_name = "Конфигурация сайта"
        verbose_name_plural = "Конфигурация сайта"

    def __str__(self):
        return "Конфигурация сайта"


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
    image_path = models.CharField(
        "Путь к изображению",
        max_length=255,
    )
    image_alt = models.CharField("Alt текста", max_length=255, blank=True, default="")

    class Meta(OrderedModel.Meta):
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Галерея"

    def __str__(self):
        return self.title


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


class PlantProduct(models.Model):
    variety_name = models.CharField("Название сорта", max_length=255)
    latin_name = models.CharField("Латинское название", max_length=255, blank=True, default="")
    article = models.CharField("Артикул", max_length=64, unique=True)
    location = models.CharField("Локация", max_length=255, blank=True, default="")
    container_type = models.CharField("Тара", max_length=120, blank=True, default="")
    order_multiple = models.PositiveIntegerField("Кратность заказа", null=True, blank=True)
    stock = models.IntegerField("Наличие", null=True, blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2, null=True, blank=True)
    discount_new = models.DecimalField("Скидка новые", max_digits=10, decimal_places=2, null=True, blank=True)
    discount_legacy = models.DecimalField("Скидка 2023-2024", max_digits=10, decimal_places=2, null=True, blank=True)
    discount_logo = models.DecimalField("Скидка з+аква лого", max_digits=10, decimal_places=2, null=True, blank=True)
    order_note = models.CharField("Заказ", max_length=255, blank=True, default="")
    description = models.TextField("Описание", blank=True, default="")
    image = models.ImageField(
        "Загруженная картинка",
        upload_to="products/%Y/%m/%d",
        blank=True,
        null=True,
    )
    image_path = models.CharField(
        "Путь к изображению",
        max_length=255,
        blank=True,
        default="",
    )
    is_published = models.BooleanField("Показывать на сайте", default=True)
    source_row = models.PositiveIntegerField("Номер строки в Excel", null=True, blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("variety_name", "article")

    def __str__(self):
        return f"{self.variety_name} ({self.article})"

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        if self.image_path:
            return static(self.image_path)
        return ""


class PriceUpload(models.Model):
    file = models.FileField("Excel файл", upload_to="price_uploads/%Y/%m/%d")
    original_filename = models.CharField("Имя файла", max_length=255)
    uploaded_by = models.ForeignKey(
        User,
        verbose_name="Кто загрузил",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="price_uploads",
    )
    uploaded_at = models.DateTimeField("Загружен", auto_now_add=True)
    update_requested = models.BooleanField("Запрошено обновление базы", default=False)
    is_merged = models.BooleanField("Изменения применены", null=True, blank=True, default=None)
    row_count = models.PositiveIntegerField("Строк в файле", default=0)
    change_summary = models.JSONField("Сводка изменений", default=dict, blank=True)
    parsed_payload = models.JSONField("Распарсенные строки", default=list, blank=True)

    class Meta:
        verbose_name = "Загрузка прайса"
        verbose_name_plural = "Загрузки прайсов"
        ordering = ("-uploaded_at",)

    def __str__(self):
        return self.original_filename

    @staticmethod
    def build_filename(moment=None):
        local_moment = timezone.localtime(moment or timezone.now())
        return local_moment.strftime("%d_%m_%Y-%H-%M-%S.xlsx")

    @property
    def display_filename(self):
        if self.original_filename and PRICE_UPLOAD_FILENAME_RE.fullmatch(self.original_filename):
            return self.original_filename
        if self.uploaded_at:
            return self.build_filename(self.uploaded_at)
        return self.original_filename

    @property
    def merge_state(self):
        if not self.update_requested:
            return "skipped"
        if self.is_merged is True:
            return "merged"
        if self.is_merged is False:
            return "cancelled"
        return "pending"
