# Generated by Django 5.1.1 on 2024-10-14 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_remove_producto_imagen_alter_producto_categoria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='productos_imagenes/'),
        ),
    ]
