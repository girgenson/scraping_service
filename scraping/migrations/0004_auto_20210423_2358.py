# Generated by Django 3.1.7 on 2021-04-23 20:58

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import scraping.models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_auto_20210330_2156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
        migrations.AlterField(
            model_name='city',
            name='slug',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='error',
            name='data',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='url',
            name='url_data',
            field=jsonfield.fields.JSONField(default=scraping.models.default_urls),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='scraping.city', verbose_name='Город'),
        ),
    ]
