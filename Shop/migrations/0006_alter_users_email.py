# Generated by Django 5.0.4 on 2024-05-18 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0005_alter_users_adresse_alter_users_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='Email',
            field=models.EmailField(max_length=132),
        ),
    ]
