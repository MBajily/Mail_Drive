# Generated by Django 4.2.1 on 2024-04-06 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_drive_file_file_alter_email_file_file_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='email',
            options={'ordering': ['-timestamp']},
        ),
    ]