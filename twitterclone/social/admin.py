from django.contrib import admin

from .models import Tweet, Profile

admin.site.register(Profile)
admin.site.register(Tweet)


