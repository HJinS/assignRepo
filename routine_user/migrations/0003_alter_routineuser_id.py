# Generated by Django 4.0.4 on 2022-05-05 06:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('routine_user', '0002_alter_routineuser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routineuser',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e938f645-dcc6-4598-8a90-03bb803cf1e6'), primary_key=True, serialize=False),
        ),
    ]