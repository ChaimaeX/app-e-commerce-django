# Generated by Django 5.0.4 on 2024-05-19 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0009_alter_users_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commande',
            name='save_by',
        ),
    ]
