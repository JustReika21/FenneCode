# Generated by Django 5.1.6 on 2025-04-05 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='user_avatars/default.jpg', upload_to='user_avatars/'),
        ),
    ]
