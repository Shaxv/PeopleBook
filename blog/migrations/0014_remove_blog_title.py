# Generated by Django 3.1.5 on 2021-02-08 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20210208_0741'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='title',
        ),
    ]
