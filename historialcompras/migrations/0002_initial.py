# Generated by Django 5.1.1 on 2025-01-02 11:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('historialcompras', '0001_initial'),
        ('pedidos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='historialcompra',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_compras', to='pedidos.pedido'),
        ),
        migrations.AddField(
            model_name='historialcompra',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_compras', to=settings.AUTH_USER_MODEL),
        ),
    ]