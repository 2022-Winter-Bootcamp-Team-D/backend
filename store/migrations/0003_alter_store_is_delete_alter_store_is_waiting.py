# Generated by Django 4.1 on 2023-01-05 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_store_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='store',
            name='is_waiting',
            field=models.BooleanField(default=False),
        ),
    ]
