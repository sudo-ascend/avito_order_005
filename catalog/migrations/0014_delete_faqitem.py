from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0013_alter_siteconfiguration_plants_eyebrow_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FAQItem",
        ),
    ]
