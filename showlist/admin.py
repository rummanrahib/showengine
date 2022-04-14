from django.contrib import admin

from .models import Review, ShowList, StreamPlatform

# Register your models here
admin.site.register(ShowList)
admin.site.register(StreamPlatform)
admin.site.register(Review)
