# Generated by Django 4.0.4 on 2022-05-03 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='category',
            field=models.CharField(max_length=10),
        ),
    ]