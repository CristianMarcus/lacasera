# Generated by Django 5.1.1 on 2025-01-02 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=100)),
                ('maintenance_mode', models.BooleanField(default=False)),
                ('support_email', models.EmailField(max_length=254)),
            ],
        ),
    ]
