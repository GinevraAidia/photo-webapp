from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_alter_event_user"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Reaction",
        ),
    ]