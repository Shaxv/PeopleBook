# Generated by Django 3.1.7 on 2021-03-17 13:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_room_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
