# Generated by Django 4.1.7 on 2023-04-25 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas_Retail', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
    ]
