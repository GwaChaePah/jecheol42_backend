# Generated by Django 3.2.8 on 2021-11-11 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20211111_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.profile'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.profile'),
        ),
    ]
