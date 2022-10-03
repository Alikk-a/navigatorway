# Generated by Django 4.0 on 2022-09-29 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naviway', '0003_targ_alter_texniki_anotacia_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cursce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cource', models.CharField(blank=True, max_length=50, null=True, verbose_name='Наименование')),
                ('koment_cource', models.TextField(blank=True, null=True, verbose_name='описание курса')),
            ],
            options={
                'verbose_name': 'Курсы описалово',
                'verbose_name_plural': 'курсы описалово',
            },
        ),
        migrations.CreateModel(
            name='Cursceteh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_cource', models.IntegerField(blank=True, null=True, verbose_name='Курс - номер')),
                ('id_tex', models.IntegerField(blank=True, null=True, verbose_name='Номер техники к курсу')),
                ('n_por', models.IntegerField(blank=True, null=True, verbose_name='Порядок в курсе')),
            ],
            options={
                'verbose_name': 'Курсы Техник',
                'verbose_name_plural': 'Курсы Техник',
            },
        ),
        migrations.CreateModel(
            name='Podhod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('podhod', models.CharField(blank=True, max_length=100, null=True, verbose_name='Подход')),
            ],
            options={
                'verbose_name': 'Подход',
                'verbose_name_plural': 'Подход',
            },
        ),
        migrations.AlterModelOptions(
            name='targ',
            options={'verbose_name': 'Цели описалово', 'verbose_name_plural': 'Цели описалово'},
        ),
        migrations.RemoveField(
            model_name='targ',
            name='id_cel',
        ),
        migrations.RemoveField(
            model_name='targ',
            name='id_texnik',
        ),
        migrations.AddField(
            model_name='targ',
            name='cel_texniki',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Наименование'),
        ),
        migrations.AddField(
            model_name='targ',
            name='koment_cel',
            field=models.TextField(blank=True, null=True, verbose_name='описание направления'),
        ),
    ]
