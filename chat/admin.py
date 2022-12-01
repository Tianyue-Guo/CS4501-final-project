from django.contrib import admin

# Register your models here.
from .models import World, Message

admin.site.register(World)
admin.site.register(Message)