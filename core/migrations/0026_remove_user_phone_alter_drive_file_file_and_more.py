# Generated by Django 4.2.1 on 2024-07-22 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.AlterField(
            model_name='drive_file',
            name='file',
            field=models.FileField(upload_to='C:\\Users\\mbaji\\django\\Mail_Drive\\media'),
        ),
        migrations.AlterField(
            model_name='email_file',
            name='file',
            field=models.FileField(upload_to='C:\\Users\\mbaji\\django\\Mail_Drive\\media'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='C:\\Users\\mbaji\\django\\Mail_Drive\\media'),
        ),
    ]
