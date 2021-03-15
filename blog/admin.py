from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Friend)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Room)