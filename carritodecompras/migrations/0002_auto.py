from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('carritodecompras', '0001_initial'),  # Asegúrate de ajustar esto según sea necesario
    ]

    operations = [
        migrations.AlterField(
            model_name='lineacarrito',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='lineacarrito',
            name='producto',
            field=models.ForeignKey(to='productos.Producto', on_delete=models.CASCADE, default=1),
        ),
        migrations.AlterField(
            model_name='lineacarrito',
            name='carrito',
            field=models.ForeignKey(to='carritodecompras.Carrito', related_name='lineas', on_delete=models.CASCADE, default=1),
        ),
    ]

