# Generated by Django 4.1.1 on 2024-02-22 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_post_image_post_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
