# Generated by Django 5.1.1 on 2024-09-05 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('historialcompras', '0001_initial'),
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialcompra',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.pedido'),
        ),
    ]
