# Generated by Django 4.0.4 on 2022-05-03 07:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_routineuser_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routineuser',
            name='account_id',
            field=models.UUIDField(default=uuid.UUID('3072978a-f9a7-460b-bd9f-93714eb2a8ca'), primary_key=True, serialize=False),
        ),
    ]