from django.contrib import admin

from .models import  Question, Choice, Comment, Notification

# Register your models here.
#admin.site.register(User)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Comment)
admin.site.register(Notification)