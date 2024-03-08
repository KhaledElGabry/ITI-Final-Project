from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','email','username','phone','address','ssn']
    list_editable=['last_name','email','phone','address','ssn']
    search_fields=['first_name']
admin.site.register(User,UserAdmin)