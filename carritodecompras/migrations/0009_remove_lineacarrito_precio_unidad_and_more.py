# Generated by Django 5.1.1 on 2024-12-28 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carritodecompras', '0008_alter_lineacarrito_cantidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineacarrito',
            name='precio_unidad',
        ),
        migrations.RemoveField(
            model_name='lineacarrito',
            name='variedad',
        ),
    ]
