# Generated by Django 4.0.4 on 2022-05-06 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine_result', '0005_alter_routineresult_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routineresult',
            name='result',
            field=models.CharField(max_length=4),
        ),
    ]
