from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0023_restore_plantproduct_admin_catalog"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="favicon",
            field=models.ImageField(
                blank=True,
                help_text="Если поле пустое, favicon будет браться из поля «Логотип сайта».",
                null=True,
                upload_to="site/branding",
                verbose_name="Favicon",
            ),
        ),
    ]
