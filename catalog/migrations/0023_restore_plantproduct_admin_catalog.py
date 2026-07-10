from django.db import migrations, models


PLANT_PRODUCTS = (
    {
        "slug": "alternanthera-reineckii-roseafolia",
        "title": "Альтернатера рейнека «Розаэфолия»",
        "latin_name": 'Alternanthera reineckii "Roseafolia"',
        "description": (
            "Акцентное красное растение для среднего и заднего плана, "
            "добавляет композиции глубину и контраст."
        ),
        "image_path": "plants/plants_1.webp",
        "image_alt": "Альтернатера рейнека Розаэфолия для аквариума Aquaklon",
        "image_width": 1122,
        "image_height": 1402,
        "image_position": "center 45%",
    },
    {
        "slug": "rotala-rotundifolia",
        "title": "Ротала ротундифолия",
        "latin_name": "Rotala rotundifolia",
        "description": (
            "Популярный стебельный вид для ярких групп, мягких переходов "
            "и плотных фоновых посадок."
        ),
        "image_path": "plants/plants_2.webp",
        "image_alt": "Ротала ротундифолия для аквариумного травника",
        "image_width": 1122,
        "image_height": 1402,
        "image_position": "center 45%",
    },
    {
        "slug": "bucephalandra",
        "title": "Буцефаландра",
        "latin_name": "Bucephalandra",
        "description": (
            "Медленнорастущее растение для коряг и камней, хорошо работает "
            "в детальных природных сценах."
        ),
        "image_path": "plants/plants_3.webp",
        "image_alt": "Буцефаландра для декора коряг и камней в аквариуме",
        "image_width": 1122,
        "image_height": 1402,
        "image_position": "center 45%",
    },
    {
        "slug": "anubias-nana",
        "title": "Анубиас нана",
        "latin_name": "Anubias nana",
        "description": (
            "Неприхотливый компактный вид с плотными листьями для переднего "
            "плана, коряг и теневых участков."
        ),
        "image_path": "plants/plants_4.webp",
        "image_alt": "Анубиас нана для переднего плана аквариума",
        "image_width": 760,
        "image_height": 580,
        "image_position": "",
    },
    {
        "slug": "cryptocoryne",
        "title": "Криптокорина",
        "latin_name": "Cryptocoryne",
        "description": (
            "Розеточное растение для стабильных композиций, хорошо смотрится "
            "группами на среднем плане."
        ),
        "image_path": "plants/plants_5.webp",
        "image_alt": "Криптокорина для среднего плана аквариума",
        "image_width": 1122,
        "image_height": 1402,
        "image_position": "center 45%",
    },
    {
        "slug": "monte-carlo",
        "title": "Монте-Карло",
        "latin_name": 'Micranthemum tweediei "Monte Carlo"',
        "description": (
            "Почвопокровное растение для плотного зеленого ковра и плавных "
            "береговых линий в акваскейпе."
        ),
        "image_path": "plants/plants_6.webp",
        "image_alt": "Монте-Карло для ковра в аквариуме",
        "image_width": 1536,
        "image_height": 1024,
        "image_position": "",
    },
    {
        "slug": "eleocharis",
        "title": "Элеохарис",
        "latin_name": "Eleocharis",
        "description": (
            "Тонкая травянистая фактура для переднего плана, полян и "
            "естественных переходов между камнями."
        ),
        "image_path": "plants/plants_7.webp",
        "image_alt": "Элеохарис для переднего плана и полян в аквариуме",
        "image_width": 1122,
        "image_height": 1402,
        "image_position": "center 45%",
    },
    {
        "slug": "ludwigia",
        "title": "Людвигия",
        "latin_name": "Ludwigia",
        "description": (
            "Выразительное стебельное растение с теплыми оттенками для "
            "цветовых акцентов в композиции."
        ),
        "image_path": "plants/plants_8.webp",
        "image_alt": "Людвигия для цветового акцента в аквариуме",
        "image_width": 760,
        "image_height": 580,
        "image_position": "",
    },
)


def seed_plant_products(apps, schema_editor):
    PlantProduct = apps.get_model("catalog", "PlantProduct")

    for index, product in enumerate(PLANT_PRODUCTS, start=1):
        PlantProduct.objects.update_or_create(
            slug=product["slug"],
            defaults={
                "title": product["title"],
                "latin_name": product["latin_name"],
                "description": product["description"],
                "image_path": product["image_path"],
                "image_alt": product["image_alt"],
                "image_width": product["image_width"],
                "image_height": product["image_height"],
                "image_position": product["image_position"],
                "sort_order": index,
                "is_published": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0022_seo_timestamps"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlantProduct",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
                ("sort_order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
                ("is_published", models.BooleanField(default=True, verbose_name="Показывать на сайте")),
                ("slug", models.SlugField(max_length=160, unique=True, verbose_name="Slug")),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("latin_name", models.CharField(blank=True, default="", max_length=255, verbose_name="Латинское название")),
                ("description", models.TextField(verbose_name="Описание")),
                ("image", models.ImageField(blank=True, null=True, upload_to="site/plants", verbose_name="Изображение")),
                ("image_path", models.CharField(blank=True, default="", max_length=255, verbose_name="Путь к изображению")),
                ("image_alt", models.CharField(blank=True, default="", max_length=255, verbose_name="Альтернативный текст")),
                ("image_width", models.PositiveIntegerField(default=1122, verbose_name="Ширина изображения")),
                ("image_height", models.PositiveIntegerField(default=1402, verbose_name="Высота изображения")),
                ("image_position", models.CharField(blank=True, default="", max_length=64, verbose_name="Позиция изображения")),
            ],
            options={
                "verbose_name": "Растение каталога",
                "verbose_name_plural": "Каталог растений",
                "ordering": ("sort_order", "id"),
            },
        ),
        migrations.RunPython(seed_plant_products, migrations.RunPython.noop),
    ]
