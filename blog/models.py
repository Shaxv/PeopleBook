from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
import json
from django.contrib.humanize.templatetags import humanize
from io import BytesIO
from django.core.files import File
from PIL import Image

def UserMethods():
    def get_date(self):
        return humanize.naturaltime(self.date_joined)
    auth.models.User.add_to_class("get_date", get_date)
UserMethods()

def make_image(image, size):
    img = Image.open(image)
    img.convert('RGB')
    img.thumbnail(size)
    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)
    image = File(thumb_io, name=image.name)
    return image


class Profile(models.Model):
    GENDER_CHOICES = (
        ('Male', "Male"),
        ('Female', "Female"),
        ('Prefer not to say', "Prefer not to say"),
    )
    COUNTRY_CHOICES = (
        ('Hungary', "Hungary"),
        ('United States', "United States"),
    )

    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, blank=True, null=True)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to="static/pics/profile_pics/", blank=True, null=True)
    background = models.ImageField(upload_to="static/pics/bg_pics/", blank=True)

    def save(self, *args, **kwargs):
        self.image = make_image(image=self.image, size=(100, 100))
        super().save(self, *args, **kwargs)

    def __str__(self):
        return f"{self.user}'s profile"


class Friend(models.Model):
    STATUS_CHOICES = (
        ('Sent', 'Sent'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", default=None)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend", default=None)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def get_date(self):
        return humanize.naturaltime(self.date_created)

    def __str__(self):
        return f"{self.user} and {self.friend}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def get_date(self):
        return humanize.naturaltime(self.date_posted)

    def __str__(self):
        return f"{self.author}'s. {self.date_posted}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name="fasz", default=None)

    def get_date(self):
        return humanize.naturaltime(self.date_posted)

    def __str__(self):
        return f"{self.post} - {self.author}"

    class Meta:
        ordering = ["-date_posted"]


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", default=None)

    def __str__(self):
        return f"{self.user} liked {self.post}"



class Room(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", default=None, null=True)
    users = models.ManyToManyField(User, default=None)
    title = models.CharField(max_length=250, default=None)
    limit = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def get_date(self):
        return humanize.naturaltime(self.date_created)

    def __str__(self):
        return self.title


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def get_date(self):
        return humanize.naturaltime(self.date_posted)