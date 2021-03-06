from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

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
    image = models.ImageField(upload_to="static/pics/profile_pics/", blank=True)
    background = models.ImageField(upload_to="static/pics/bg_pics/", blank=True)

    def __str__(self):
        return f"{self.user}'s profile"


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", default=None)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend", default=None)

    def __str__(self):
        return f"{self.user} and {self.friend}"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author}'s. {self.date_posted}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name="fasz", default=None)

    def __str__(self):
        return f"{self.post} - {self.author}"

    class Meta:
        ordering = ["-date_posted"]

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", default=None)

    def __str__(self):
        return f"{self.user} liked {self.post}"