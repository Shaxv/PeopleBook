# Generated by Django 3.1.5 on 2021-02-28 20:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0019_like_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='likes',
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(default=None, related_name='fasz', to=settings.AUTH_USER_MODEL),
        ),
    ]
