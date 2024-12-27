# Generated by Django 5.1.1 on 2024-12-23 19:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carritodecompras', '0003_lineacarrito_precio_unidad_lineacarrito_variedad_and_more'),
        ('productos', '0002_producto_precio_docena_producto_precio_unidad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineacarrito',
            name='variedad',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='productos.variedadempanada'),
        ),
    ]