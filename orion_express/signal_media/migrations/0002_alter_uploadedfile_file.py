# Generated by Django 4.2.5 on 2023-09-29 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signal_media', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(upload_to='kzpl/final/temp/input/'),
        ),
    ]
