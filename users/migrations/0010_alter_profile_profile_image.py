# Generated by Django 4.2.7 on 2023-12-09 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(default='', upload_to='profiles/'),
        ),
    ]
