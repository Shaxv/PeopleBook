from django.contrib.auth.models import User
from django import template

register = template.Library()

@register.filter
def filterUser(id):
    return User.objects.filter(id=id)

@register.filter
def setVal(val=None):
    return val

