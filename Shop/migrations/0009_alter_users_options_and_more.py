# Generated by Django 5.0.4 on 2024-05-19 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0008_rename_email_users_gmail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'users'},
        ),
        migrations.RemoveField(
            model_name='commandeproduct',
            name='price_finich',
        ),
        migrations.RemoveField(
            model_name='commandeproduct',
            name='total_a',
        ),
    ]
