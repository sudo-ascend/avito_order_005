import catalog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0018_remove_siteconfiguration_about_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="delivery_terms_file",
            field=models.FileField(
                blank=True,
                null=True,
                storage=catalog.models.OverwriteStorage(),
                upload_to=catalog.models.upload_delivery_terms_file,
                verbose_name="Условия заказа и доставки",
            ),
        ),
        migrations.AddField(
            model_name="siteconfiguration",
            name="delivery_terms_file_original_name",
            field=models.CharField(
                blank=True,
                default="",
                max_length=255,
                verbose_name="Имя файла с условиями заказа и доставки",
            ),
        ),
    ]
