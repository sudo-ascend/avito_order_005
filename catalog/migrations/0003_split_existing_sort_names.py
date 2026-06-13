from django.db import migrations


def split_sort_name(raw_name: str) -> tuple[str, str]:
    raw_name = (raw_name or "").strip()
    if not raw_name:
        return "", ""

    first_open = raw_name.find("(")
    last_close = raw_name.rfind(")")
    if first_open == -1 or last_close == -1 or first_open >= last_close:
        return raw_name, ""

    latin_name = raw_name[:first_open].strip()
    russian_name = raw_name[first_open + 1:last_close].strip()
    return russian_name or raw_name, latin_name


def forward(apps, schema_editor):
    PlantProduct = apps.get_model("catalog", "PlantProduct")
    for product in PlantProduct.objects.all():
        if product.latin_name:
            continue
        russian_name, latin_name = split_sort_name(product.variety_name)
        if russian_name != product.variety_name or latin_name:
            product.variety_name = russian_name
            product.latin_name = latin_name
            product.save(update_fields=["variety_name", "latin_name"])


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_plantproduct_image_alter_plantproduct_image_path"),
    ]

    operations = [
        migrations.RunPython(forward, migrations.RunPython.noop),
    ]
