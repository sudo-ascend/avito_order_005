from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TXT_PATH = ROOT / "yandex_webmaster_queries_top500.txt"
CSV_PATH = ROOT / "yandex_webmaster_queries_top500.csv"
MAX_QUERIES = 500


CORE_PHRASES = [
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
    "растения для акваскейпа",
    "растения для запуска аквариума",
    "почвопокровные растения для аквариума",
    "растения для переднего плана аквариума",
    "растения для заднего плана аквариума",
    "растения на корягу в аквариум",
    "растения на камни в аквариум",
]

COMMERCIAL_TEMPLATES = [
    "купить {x}",
    "заказать {x}",
    "где купить {x}",
    "{x} цена",
    "{x} цены",
    "{x} наличие",
    "{x} каталог",
    "{x} доставка",
]

GEO_TAILS = [
    "в москве",
    "по москве",
    "по московской области",
    "в москве с доставкой",
]

BRAND_QUERIES = [
    "aquaklon",
    "акваклон",
    "aquaklon аквариумные растения",
    "акваклон аквариумные растения",
    "aquaklon меристемные растения",
    "акваклон меристемные растения",
    "aquaklon растения для аквариума",
    "акваклон растения для аквариума",
    "aquaklon in vitro",
    "акваклон in vitro",
    "aquaklon купить",
    "акваклон купить",
    "aquaklon цена",
    "акваклон цена",
    "aquaklon каталог",
    "акваклон каталог",
    "aquaklon доставка",
    "акваклон доставка",
    "aquaklon отзывы",
    "акваклон отзывы",
]

SPECIES = [
    "альтернатера рейнека розаэфолия",
    "ротала ротундифолия",
    "буцефаландра",
    "анубиас нана",
    "криптокорина",
    "монте карло",
    "элеохарис",
    "людвигия",
]

SPECIES_TEMPLATES = [
    "купить {x}",
    "{x} цена",
    "{x} для аквариума",
    "{x} in vitro",
    "{x} меристема",
    "купить {x} в москве",
    "{x} с доставкой",
]

COMPETITOR_QUERIES = [
    "mikroklon.ru аквариумные растения",
    "mikroklon.ru меристемные растения",
    "микроклон аквариумные растения",
    "микроклон меристемные растения",
    "aquaklon или mikroklon",
    "что лучше aquaklon или mikroklon",
    "аналог mikroklon.ru аквариумные растения",
    "альтернатива mikroklon.ru",
]


queries: list[tuple[str, str]] = []
seen: set[str] = set()


def normalize(text: str) -> str:
    text = text.replace("«", " ").replace("»", " ").replace('"', " ")
    text = re.sub(r"\s+", " ", text).strip(" ,.-").lower()
    return text


def add(query: str, group: str) -> None:
    query_n = normalize(query)
    if not query_n or query_n in seen:
        return
    seen.add(query_n)
    queries.append((query_n, group))


for query in BRAND_QUERIES:
    add(query, "brand")

for phrase in CORE_PHRASES:
    for template in COMMERCIAL_TEMPLATES:
        add(template.format(x=phrase), "core")
    for geo in GEO_TAILS:
        add(f"{phrase} {geo}", "core_geo")
        add(f"купить {phrase} {geo}", "core_geo")
        add(f"{phrase} {geo} цена", "core_geo")

for species in SPECIES:
    for template in SPECIES_TEMPLATES:
        add(template.format(x=species), "species")

for query in COMPETITOR_QUERIES:
    add(query, "competitor")

# добивка до 500 за счет самых релевантных длинных хвостов
for phrase in CORE_PHRASES:
    for geo in GEO_TAILS:
        for tail in [
            "для акваскейпа",
            "для травника",
            "без улиток",
            "без водорослей",
            "in vitro",
            "для запуска аквариума",
            "для переднего плана",
            "для заднего плана",
        ]:
            add(f"купить {phrase} {tail} {geo}", "longtail")
            add(f"{phrase} {tail} {geo} цена", "longtail")
            add(f"заказать {phrase} {tail} {geo}", "longtail")
            if len(queries) >= MAX_QUERIES:
                break
        if len(queries) >= MAX_QUERIES:
            break
    if len(queries) >= MAX_QUERIES:
        break

queries = queries[:MAX_QUERIES]

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
