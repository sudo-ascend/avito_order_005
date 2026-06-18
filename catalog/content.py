from dataclasses import dataclass


@dataclass(frozen=True)
class PlantProduct:
    slug: str
    title: str
    latin_name: str
    description: str
    image_path: str
    image_alt: str
    image_width: int
    image_height: int
    image_position: str = ""


PLANT_PRODUCTS: tuple[PlantProduct, ...] = (
    PlantProduct(
        slug="alternanthera-reineckii-roseafolia",
        title="Альтернатера рейнека «Розаэфолия»",
        latin_name='Alternanthera reineckii "Roseafolia"',
        description=(
            "Акцентное красное растение для среднего и заднего плана, "
            "добавляет композиции глубину и контраст."
        ),
        image_path="plants/plants_1.webp",
        image_alt="Альтернатера рейнека Розаэфолия для аквариума Aquaklon",
        image_width=1122,
        image_height=1402,
        image_position="center 45%",
    ),
    PlantProduct(
        slug="rotala-rotundifolia",
        title="Ротала ротундифолия",
        latin_name="Rotala rotundifolia",
        description=(
            "Популярный стебельный вид для ярких групп, мягких переходов "
            "и плотных фоновых посадок."
        ),
        image_path="plants/plants_2.webp",
        image_alt="Ротала ротундифолия для аквариумного травника",
        image_width=1122,
        image_height=1402,
        image_position="center 45%",
    ),
    PlantProduct(
        slug="bucephalandra",
        title="Буцефаландра",
        latin_name="Bucephalandra",
        description=(
            "Медленнорастущее растение для коряг и камней, хорошо работает "
            "в детальных природных сценах."
        ),
        image_path="plants/plants_3.webp",
        image_alt="Буцефаландра для декора коряг и камней в аквариуме",
        image_width=1122,
        image_height=1402,
        image_position="center 45%",
    ),
    PlantProduct(
        slug="anubias-nana",
        title="Анубиас нана",
        latin_name="Anubias nana",
        description=(
            "Неприхотливый компактный вид с плотными листьями для переднего "
            "плана, коряг и теневых участков."
        ),
        image_path="plants/plants_4.webp",
        image_alt="Анубиас нана для переднего плана аквариума",
        image_width=760,
        image_height=580,
    ),
    PlantProduct(
        slug="cryptocoryne",
        title="Криптокорина",
        latin_name="Cryptocoryne",
        description=(
            "Розеточное растение для стабильных композиций, хорошо смотрится "
            "группами на среднем плане."
        ),
        image_path="plants/plants_5.webp",
        image_alt="Криптокорина для среднего плана аквариума",
        image_width=1122,
        image_height=1402,
        image_position="center 45%",
    ),
    PlantProduct(
        slug="monte-carlo",
        title="Монте-Карло",
        latin_name='Micranthemum tweediei "Monte Carlo"',
        description=(
            "Почвопокровное растение для плотного зелёного ковра и плавных "
            "береговых линий в акваскейпе."
        ),
        image_path="plants/plants_6.webp",
        image_alt="Монте-Карло для ковра в аквариуме",
        image_width=1536,
        image_height=1024,
    ),
    PlantProduct(
        slug="eleocharis",
        title="Элеохарис",
        latin_name="Eleocharis",
        description=(
            "Тонкая травянистая фактура для переднего плана, полян и "
            "естественных переходов между камнями."
        ),
        image_path="plants/plants_7.webp",
        image_alt="Элеохарис для переднего плана и полян в аквариуме",
        image_width=1122,
        image_height=1402,
        image_position="center 45%",
    ),
    PlantProduct(
        slug="ludwigia",
        title="Людвигия",
        latin_name="Ludwigia",
        description=(
            "Выразительное стебельное растение с тёплыми оттенками для "
            "цветовых акцентов в композиции."
        ),
        image_path="plants/plants_8.webp",
        image_alt="Людвигия для цветового акцента в аквариуме",
        image_width=760,
        image_height=580,
    ),
)
