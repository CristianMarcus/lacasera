# Generated by Django 5.1.1 on 2024-12-26 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carritodecompras', '0007_alter_lineacarrito_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineacarrito',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
