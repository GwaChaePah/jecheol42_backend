# Generated by Django 3.2.8 on 2021-11-14 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_alter_post_image1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='local',
            new_name='region',
        ),
    ]