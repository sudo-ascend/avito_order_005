from django.db import migrations


def sync_logo_to_favicon(apps, schema_editor):
    SiteConfiguration = apps.get_model("catalog", "SiteConfiguration")
    for config in SiteConfiguration.objects.exclude(logo="").exclude(logo__isnull=True):
        if not config.favicon:
            config.favicon = config.logo
            config.save(update_fields=["favicon"])


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0024_siteconfiguration_favicon"),
    ]

    operations = [
        migrations.RunPython(sync_logo_to_favicon, migrations.RunPython.noop),
    ]
