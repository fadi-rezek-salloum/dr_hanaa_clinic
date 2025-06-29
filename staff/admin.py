from django.contrib import admin
from taggit.models import Tag

from .models import Staff

admin.site.register(Staff)
admin.site.unregister(Tag)
