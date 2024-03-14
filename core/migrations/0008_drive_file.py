# Generated by Django 4.2.1 on 2024-03-14 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_delete_drive_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drive_File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='C:\\Users\\mbaji\\Desktop\\Django Projects\\mail_drive\\project\\media')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('archived', models.BooleanField(default=False)),
                ('starred', models.BooleanField(blank=True, default=False)),
                ('deleted', models.BooleanField(blank=True, default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
