from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(Skill)
admin.site.register(Notification)