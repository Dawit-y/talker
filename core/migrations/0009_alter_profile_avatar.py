# Generated by Django 4.2.3 on 2023-10-16 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default.png', null=True, upload_to=''),
        ),
    ]
