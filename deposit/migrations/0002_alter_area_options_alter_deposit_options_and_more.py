# Generated by Django 4.0.2 on 2022-02-14 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='area',
            options={'managed': False, 'ordering': ['name'], 'verbose_name': 'Район', 'verbose_name_plural': 'Районы'},
        ),
        migrations.AlterModelOptions(
            name='deposit',
            options={'managed': False, 'ordering': ['id'], 'verbose_name': 'Месторождение', 'verbose_name_plural': 'Месторождения'},
        ),
        migrations.AlterModelOptions(
            name='enterprise',
            options={'managed': False, 'ordering': ['id'], 'verbose_name': 'Недропользователь', 'verbose_name_plural': 'Недропользователи'},
        ),
        migrations.AlterModelOptions(
            name='license',
            options={'managed': False, 'ordering': ['id'], 'verbose_name': 'Лицензия', 'verbose_name_plural': 'Лицензии'},
        ),
        migrations.AlterModelOptions(
            name='municipality',
            options={'managed': False, 'ordering': ['id_deposit'], 'verbose_name': 'Населенный пункт', 'verbose_name_plural': 'Населенные пункты'},
        ),
        migrations.AlterModelOptions(
            name='municipalitytype',
            options={'managed': False, 'ordering': ['name'], 'verbose_name': 'Тип населенных пунктов', 'verbose_name_plural': 'Типы населенных пунктов'},
        ),
    ]
