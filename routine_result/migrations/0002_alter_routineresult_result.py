# Generated by Django 4.0.4 on 2022-05-05 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine_result', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routineresult',
            name='result',
            field=models.CharField(choices=[('N', 'NOT'), ('T', 'TRY'), ('D', 'DONE')], default='N', max_length=1),
        ),
    ]