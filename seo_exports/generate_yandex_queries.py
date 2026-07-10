from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TXT_PATH = ROOT / "yandex_webmaster_queries_10000.txt"
CSV_PATH = ROOT / "yandex_webmaster_queries_10000.csv"
MAX_QUERIES = 10_000


AQUARIUM_PHRASES = [
    "аквариумные растения",
    "растения для аквариума",
    "меристемные аквариумные растения",
    "меристемные растения для аквариума",
    "микроклон аквариумных растений",
    "микроклонные аквариумные растения",
    "растения in vitro для аквариума",
    "стерильные растения для аквариума",
    "чистые растения для аквариума",
    "живые растения для аквариума",
    "растения без улиток для аквариума",
    "растения без водорослей для аквариума",
    "растения для травника",
    "растения для запуска травника",
    "растения для акваскейпа",
    "растения для растительного аквариума",
    "растения для нано аквариума",
    "растения для креветочника",
    "растения для природного аквариума",
    "растения для голландского аквариума",
    "растения для оформления аквариума",
    "растения для аквариумного дизайна",
    "растения для домашнего аквариума",
    "растения для профессионального аквариума",
    "растения для запуска аквариума",
    "растения для нового аквариума",
    "растения для чистого старта аквариума",
    "растения для переднего плана аквариума",
    "растения для среднего плана аквариума",
    "растения для заднего плана аквариума",
    "почвопокровные растения для аквариума",
    "стебельные растения для аквариума",
    "красные растения для аквариума",
    "компактные растения для аквариума",
    "неприхотливые растения для аквариума",
    "растения на корягу в аквариум",
    "растения на камни в аквариум",
    "растения для красивого аквариума",
    "растения для здорового аквариума",
    "растения для плотной посадки аквариума",
    "растения для декоративного аквариума",
    "растения для современного аквариума",
    "растения для конкурсного акваскейпа",
    "аквариумные растения в баночке",
    "аквариумные растения в контейнере",
    "аквариумные растения для московского региона",
    "меристема для аквариума",
    "микроклон для аквариума",
    "посадочный материал для аквариума",
    "чистый посадочный материал для аквариума",
]

GEOS = [
    "в москве",
    "по москве",
    "по московской области",
    "в москве с доставкой",
    "по москве с доставкой",
    "для москвы и области",
]

USE_CASES = [
    "для акваскейпа",
    "для травника",
    "для запуска аквариума",
    "для нового аквариума",
    "для переднего плана",
    "для среднего плана",
    "для заднего плана",
    "для нано аквариума",
    "для креветочника",
    "для природного аквариума",
    "для голландского аквариума",
    "для оформления аквариума",
    "для аквариумного дизайна",
    "для плотной посадки",
    "для чистого старта",
    "для красивого аквариума",
    "для здорового аквариума",
    "для домашнего аквариума",
    "для профессионального аквариума",
    "для посадки на корягу",
    "для посадки на камни",
]

BENEFITS = [
    "без улиток",
    "без водорослей",
    "стерильные",
    "in vitro",
    "в баночке",
    "в контейнере",
    "с чистым стартом",
    "для быстрой посадки",
    "для аккуратной посадки",
    "для безопасного запуска",
    "для плотного ковра",
    "для яркого акцента",
]

VOLUMES = [
    "для аквариума 20 литров",
    "для аквариума 30 литров",
    "для аквариума 40 литров",
    "для аквариума 50 литров",
    "для аквариума 60 литров",
    "для аквариума 80 литров",
    "для аквариума 100 литров",
    "для аквариума 120 литров",
    "для аквариума 200 литров",
]

COMMERCIAL_TEMPLATES = [
    "купить {x}",
    "заказать {x}",
    "где купить {x}",
    "где заказать {x}",
    "{x} цена",
    "{x} цены",
    "{x} стоимость",
    "{x} прайс",
    "{x} наличие",
    "{x} каталог",
    "{x} отзывы",
    "{x} доставка",
    "{x} в наличии",
]

INFORMATIONAL_TEMPLATES = [
    "как выбрать {x}",
    "как заказать {x}",
    "как купить {x}",
    "как посадить {x}",
    "как сажать {x}",
    "{x} для начинающих",
    "{x} для чистого запуска",
    "{x} что выбрать",
    "{x} как оформить заказ",
    "{x} для красивого аквариума",
    "{x} для здорового аквариума",
]

BRAND_QUERIES = [
    "aquaklon",
    "акваклон",
    "aquaklon москва",
    "акваклон москва",
    "aquaklon аквариумные растения",
    "акваклон аквариумные растения",
    "aquaklon meristem",
    "aquaklon in vitro",
    "aquaklon mericlone aquarium plants",
    "акваклон микроклонные растения",
    "aquaklon для травника",
    "акваклон для травника",
    "aquaklon для акваскейпа",
    "акваклон для акваскейпа",
    "aquaklon купить",
    "акваклон купить",
    "aquaklon заказать",
    "акваклон заказать",
    "aquaklon цена",
    "акваклон цена",
    "aquaklon цены",
    "акваклон цены",
    "aquaklon прайс",
    "акваклон прайс",
    "aquaklon каталог",
    "акваклон каталог",
    "aquaklon наличие",
    "акваклон наличие",
    "aquaklon доставка",
    "акваклон доставка",
    "aquaklon отзывы",
    "акваклон отзывы",
    "aquaklon в москве",
    "акваклон в москве",
    "aquaklon по москве",
    "акваклон по москве",
    "aquaklon по московской области",
    "акваклон по московской области",
    "aquaklon меристемные растения",
    "акваклон меристемные растения",
    "aquaklon меристемные аквариумные растения",
    "акваклон меристемные аквариумные растения",
    "aquaklon аквариумные растения in vitro",
    "акваклон аквариумные растения in vitro",
    "aquaklon растения без улиток",
    "акваклон растения без улиток",
    "aquaklon растения без водорослей",
    "акваклон растения без водорослей",
    "aquaklon для запуска аквариума",
    "акваклон для запуска аквариума",
]

COMPETITOR_VARIANTS = [
    "mikroklon",
    "mikroklon.ru",
    "микроклон",
    "микроклон ру",
]

COMPETITOR_TEMPLATES = [
    "{c} аквариумные растения",
    "{c} меристемные растения",
    "{c} растения in vitro",
    "{c} микроклонные растения",
    "{c} цена",
    "{c} цены",
    "{c} каталог",
    "{c} отзывы",
    "{c} доставка",
    "аналог {c} аквариумные растения",
    "альтернатива {c}",
    "что лучше aquaklon или {c}",
    "aquaklon или {c}",
    "сравнение aquaklon и {c}",
    "{c} или aquaklon",
    "где купить как на {c}",
]

FAQ_SEEDS = [
    "как выбрать меристемные растения для аквариума",
    "как выбрать микроклонные растения для аквариума",
    "как посадить аквариумные растения in vitro",
    "как сажать меристемные растения в аквариум",
    "какие аквариумные растения подойдут для запуска аквариума",
    "какие растения для акваскейпа купить в москве",
    "где купить чистые аквариумные растения без улиток",
    "как заказать аквариумные растения с доставкой по москве",
    "как выбрать растения для переднего плана аквариума",
    "как выбрать растения для заднего плана аквариума",
    "какие растения in vitro лучше для травника",
    "что купить для красивого аквариума с живыми растениями",
    "как оформить заказ на растения для аквариума aquaklon",
    "как выбрать растения для нано аквариума",
    "как выбрать растения для креветочника",
    "какие растения на корягу купить для аквариума",
    "какие растения на камни купить для аквариума",
    "как выбрать почвопокровные растения для аквариума",
    "как выбрать красные аквариумные растения",
    "какие стерильные растения лучше для запуска травника",
    "как выбрать растения без водорослей для аквариума",
]

SPECIES = [
    {
        "group": "species_alternanthera",
        "names": [
            "альтернатера рейнека розаэфолия",
            "alternanthera reineckii roseafolia",
            'alternanthera reineckii "roseafolia"',
        ],
        "uses": [
            "для среднего плана",
            "для заднего плана",
            "красное растение для аквариума",
            "для акваскейпа",
            "для травника",
        ],
    },
    {
        "group": "species_rotala",
        "names": ["ротала ротундифолия", "rotala rotundifolia"],
        "uses": [
            "для заднего плана",
            "для травника",
            "для акваскейпа",
            "для густой посадки",
            "для цветового перехода",
        ],
    },
    {
        "group": "species_bucephalandra",
        "names": ["буцефаландра", "bucephalandra"],
        "uses": [
            "на корягу",
            "на камни",
            "для природного аквариума",
            "для акваскейпа",
            "для декоративного аквариума",
        ],
    },
    {
        "group": "species_anubias",
        "names": ["анубиас нана", "anubias nana"],
        "uses": [
            "для переднего плана",
            "на корягу",
            "для теневых участков",
            "для нано аквариума",
            "для стабильного аквариума",
        ],
    },
    {
        "group": "species_cryptocoryne",
        "names": ["криптокорина", "cryptocoryne"],
        "uses": [
            "для среднего плана",
            "для стабильного аквариума",
            "для групповой посадки",
            "для травника",
            "для нового аквариума",
        ],
    },
    {
        "group": "species_montecarlo",
        "names": [
            "монте карло",
            "micranthemum tweediei monte carlo",
            "micranthemum monte carlo",
        ],
        "uses": [
            "для ковра в аквариуме",
            "для переднего плана",
            "для акваскейпа",
            "для нано аквариума",
            "для плотного ковра",
        ],
    },
    {
        "group": "species_eleocharis",
        "names": ["элеохарис", "eleocharis"],
        "uses": [
            "для переднего плана",
            "для полян в аквариуме",
            "для акваскейпа",
            "для ковра в аквариуме",
            "для нано аквариума",
        ],
    },
    {
        "group": "species_ludwigia",
        "names": ["людвигия", "ludwigia"],
        "uses": [
            "для цветового акцента",
            "для заднего плана",
            "красное растение для аквариума",
            "для травника",
            "для акваскейпа",
        ],
    },
]


def normalize(text: str) -> str:
    text = text.replace("«", " ").replace("»", " ").replace('"', " ")
    text = re.sub(r"\s+", " ", text).strip(" ,.-").lower()
    return text


def combine(head: str, tail: str) -> str:
    head_n = normalize(head)
    tail_n = normalize(tail)
    if not tail_n:
        return head_n
    if tail_n in head_n:
        return head_n
    return normalize(f"{head_n} {tail_n}")


queries: list[tuple[str, str]] = []
seen: set[str] = set()


def add(query: str, group: str) -> None:
    query_n = normalize(query)
    if not query_n:
        return
    if len(query_n) < 8 or len(query_n) > 130:
        return
    if query_n in seen:
        return
    seen.add(query_n)
    queries.append((query_n, group))


for query in BRAND_QUERIES:
    add(query, "brand")

for query in FAQ_SEEDS:
    add(query, "faq_seed")

for variant in COMPETITOR_VARIANTS:
    for template in COMPETITOR_TEMPLATES:
        add(template.format(c=variant), "competitor")

for phrase in AQUARIUM_PHRASES:
    for template in COMMERCIAL_TEMPLATES:
        add(template.format(x=phrase), "core_commercial")
    for template in INFORMATIONAL_TEMPLATES:
        add(template.format(x=phrase), "core_info")

    for geo in GEOS:
        phrase_geo = combine(phrase, geo)
        add(phrase_geo, "core_geo")
        add(f"купить {phrase_geo}", "core_geo")
        add(f"заказать {phrase_geo}", "core_geo")
        add(f"где купить {phrase_geo}", "core_geo")
        add(f"{phrase_geo} цена", "core_geo")
        add(f"{phrase_geo} наличие", "core_geo")

    for use_case in USE_CASES:
        phrase_use = combine(phrase, use_case)
        add(phrase_use, "core_use")
        add(f"купить {phrase_use}", "core_use")
        add(f"заказать {phrase_use}", "core_use")
        add(f"где купить {phrase_use}", "core_use")
        add(f"{phrase_use} цена", "core_use")
        add(f"{phrase_use} отзывы", "core_use")
        add(f"как выбрать {phrase_use}", "core_use")
        add(f"как посадить {phrase_use}", "core_use")
        for geo in GEOS:
            phrase_use_geo = combine(phrase_use, geo)
            add(phrase_use_geo, "core_use_geo")
            add(f"купить {phrase_use_geo}", "core_use_geo")
            add(f"заказать {phrase_use_geo}", "core_use_geo")
            add(f"{phrase_use_geo} цена", "core_use_geo")

    for benefit in BENEFITS:
        phrase_benefit = combine(phrase, benefit)
        add(phrase_benefit, "core_benefit")
        add(f"купить {phrase_benefit}", "core_benefit")
        add(f"заказать {phrase_benefit}", "core_benefit")
        add(f"{phrase_benefit} цена", "core_benefit")
        add(f"{phrase_benefit} отзывы", "core_benefit")
        add(f"как выбрать {phrase_benefit}", "core_benefit")
        for geo in GEOS:
            phrase_benefit_geo = combine(phrase_benefit, geo)
            add(phrase_benefit_geo, "core_benefit_geo")
            add(f"купить {phrase_benefit_geo}", "core_benefit_geo")
            add(f"{phrase_benefit_geo} цена", "core_benefit_geo")

    for volume in VOLUMES:
        phrase_volume = combine(phrase, volume)
        add(phrase_volume, "core_volume")
        add(f"купить {phrase_volume}", "core_volume")
        add(f"заказать {phrase_volume}", "core_volume")
        add(f"{phrase_volume} цена", "core_volume")
        add(f"как выбрать {phrase_volume}", "core_volume")

for item in SPECIES:
    for name in item["names"]:
        for template in COMMERCIAL_TEMPLATES:
            add(template.format(x=name), item["group"])
        for template in INFORMATIONAL_TEMPLATES:
            add(template.format(x=name), item["group"])
        add(f"{name} для аквариума", item["group"])
        add(f"{name} in vitro", item["group"])
        add(f"{name} меристема", item["group"])
        add(f"{name} микроклон", item["group"])
        for geo in GEOS:
            name_geo = combine(name, geo)
            add(name_geo, item["group"])
            add(f"купить {name_geo}", item["group"])
            add(f"{name_geo} цена", item["group"])
        for benefit in BENEFITS:
            name_benefit = combine(name, benefit)
            add(name_benefit, item["group"])
            add(f"купить {name_benefit}", item["group"])
            add(f"{name_benefit} цена", item["group"])
        for use_case in item["uses"]:
            name_use = combine(name, use_case)
            add(name_use, item["group"])
            add(f"купить {name_use}", item["group"])
            add(f"заказать {name_use}", item["group"])
            add(f"где купить {name_use}", item["group"])
            add(f"{name_use} цена", item["group"])
            add(f"{name_use} отзывы", item["group"])
            add(f"как выбрать {name_use}", item["group"])
            add(f"как посадить {name_use}", item["group"])
            for geo in GEOS:
                name_use_geo = combine(name_use, geo)
                add(name_use_geo, item["group"])
                add(f"купить {name_use_geo}", item["group"])
                add(f"{name_use_geo} цена", item["group"])

for phrase in AQUARIUM_PHRASES:
    for use_case in USE_CASES:
        phrase_use = combine(phrase, use_case)
        for benefit in BENEFITS:
            phrase_combo = combine(phrase_use, benefit)
            add(phrase_combo, "longtail_combo")
            add(f"купить {phrase_combo}", "longtail_combo")
            add(f"заказать {phrase_combo}", "longtail_combo")
            add(f"{phrase_combo} цена", "longtail_combo")
            add(f"как выбрать {phrase_combo}", "longtail_combo")
            add(f"как посадить {phrase_combo}", "longtail_combo")
            for geo in GEOS:
                phrase_combo_geo = combine(phrase_combo, geo)
                add(phrase_combo_geo, "longtail_combo_geo")
                add(f"купить {phrase_combo_geo}", "longtail_combo_geo")
                add(f"{phrase_combo_geo} цена", "longtail_combo_geo")
            for volume in VOLUMES:
                phrase_combo_volume = combine(phrase_combo, volume)
                add(phrase_combo_volume, "longtail_combo_volume")
                add(f"купить {phrase_combo_volume}", "longtail_combo_volume")
                add(f"{phrase_combo_volume} цена", "longtail_combo_volume")
        if len(queries) >= MAX_QUERIES * 2:
            break
    if len(queries) >= MAX_QUERIES * 2:
        break

queries = queries[:MAX_QUERIES]
group_counts = Counter(group for _query, group in queries)

with TXT_PATH.open("w", encoding="utf-8", newline="\n") as txt_file:
    for query, _group in queries:
        txt_file.write(query + "\n")

with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=";")
    writer.writerow(["query", "group"])
    writer.writerows(queries)

print(f"saved {len(queries)} queries")
print(TXT_PATH)
print(CSV_PATH)
for group, count in group_counts.most_common():
    print(f"{group}: {count}")
