# Generated by Django 5.0.4 on 2024-05-20 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0013_produit_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/img'),
        ),
    ]
