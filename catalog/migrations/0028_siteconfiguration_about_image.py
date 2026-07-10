from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0027_alter_siteconfiguration_social_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="about_image",
            field=models.ImageField(blank=True, null=True, upload_to="site/sections", verbose_name="Изображение для блока О нас"),
        ),
    ]
