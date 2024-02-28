from django.contrib import admin
from .models  import Cars
# Register your models here.

class CarsAdmin(admin.ModelAdmin):
    list_display=['name','prise','Categories']
    list_editable=['prise','Categories']
    search_fields=['name']
    list_filter=['Categories']
 
admin.site.register(Cars,CarsAdmin)

