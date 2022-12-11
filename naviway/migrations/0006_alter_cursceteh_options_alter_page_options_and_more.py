# Generated by Django 4.0 on 2022-12-07 19:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naviway', '0005_targetteh'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cursceteh',
            options={'verbose_name': 'Связь Курсов и техник', 'verbose_name_plural': 'Связь Курсов и техник'},
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'verbose_name': 'Контентные страницы', 'verbose_name_plural': 'основные страницы'},
        ),
        migrations.AlterModelOptions(
            name='targ',
            options={'verbose_name': 'Направления техник', 'verbose_name_plural': 'Направления техник'},
        ),
        migrations.AlterModelOptions(
            name='targetteh',
            options={'verbose_name': 'Связь Направлений и техник', 'verbose_name_plural': 'Связь Направлений и техник'},
        ),
        migrations.AlterField(
            model_name='page',
            name='sort',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(300)], verbose_name='сортировка'),
        ),
    ]
