from django.contrib import admin

# Register your models here.

from .models import Guitar, Performing, Musician, Photo

admin.site.register(Guitar)
admin.site.register(Performing)
admin.site.register(Musician)
admin.site.register(Photo)