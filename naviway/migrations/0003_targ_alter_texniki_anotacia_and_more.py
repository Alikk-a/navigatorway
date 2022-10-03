# Generated by Django 4.0 on 2022-09-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naviway', '0002_texniki_alter_page_options_alter_page_menuname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Targ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_texnik', models.IntegerField(blank=True, null=True, verbose_name='Техника - номер')),
                ('id_cel', models.IntegerField(blank=True, null=True, verbose_name='цель техники')),
            ],
            options={
                'verbose_name': 'Цели Техник',
                'verbose_name_plural': 'Цели Техник',
            },
        ),
        migrations.AlterField(
            model_name='texniki',
            name='anotacia',
            field=models.TextField(blank=True, null=True, verbose_name='Анотация'),
        ),
        migrations.AlterField(
            model_name='texniki',
            name='koment_spec',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий специалиста'),
        ),
    ]
