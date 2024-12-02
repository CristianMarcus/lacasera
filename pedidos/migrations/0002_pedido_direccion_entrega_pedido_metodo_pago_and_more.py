# Generated by Django 5.1.1 on 2024-11-26 17:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
        ('productos', '0007_alter_producto_imagen'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='direccion_entrega',
            field=models.CharField(default='Direccion no especificada', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='metodo_pago',
            field=models.CharField(default='direccion no especificada', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('En Preparación', 'En Preparación'), ('En Camino', 'En Camino'), ('Entregado', 'Entregado')], default='Pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedidos.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='productos',
            field=models.ManyToManyField(through='pedidos.DetallePedido', to='productos.producto'),
        ),
        migrations.DeleteModel(
            name='LineaPedido',
        ),
    ]
