from django.contrib import admin

from .models import Box, BoxVersion

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'description', 'downloads', 
        'last_download_at']
    list_filter = ['creator', 'last_download_at', ]    
    search_fields = ['name', 'description']    
    ordering = ['name', ] 

@admin.register(BoxVersion)
class BoxVersionAdmin(admin.ModelAdmin):
    list_display = ['box', 'name', 'kind', 'created_at', 'file']
    list_filter = ['kind', 'created_at']    
    search_fields = ['name', 'description', ]    
    ordering = ['name', ] 
