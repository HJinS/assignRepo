# Generated by Django 4.0.4 on 2022-05-03 02:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('routine_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=8)),
                ('goal', models.CharField(max_length=50)),
                ('is_alarm', models.BooleanField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('modified_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
