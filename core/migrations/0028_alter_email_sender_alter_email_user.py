# Generated by Django 4.2.1 on 2024-08-10 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='sender',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='email',
            name='user',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
