# Generated by Django 4.2.1 on 2024-03-13 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_user_name_user_first_name_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='C:\\Users\\mbaji\\Desktop\\Django Projects\\mail_drive\\project\\media'),
        ),
    ]
