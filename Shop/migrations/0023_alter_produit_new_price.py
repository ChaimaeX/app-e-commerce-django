# Generated by Django 5.0.6 on 2024-05-28 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0022_produit_new_price_produit_promo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='new_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
