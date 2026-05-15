from django.contrib import admin
from .models import Track

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
from .models import RiyadhAsSalihin

@admin.register(RiyadhAsSalihin)
class RiyadhAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'created_at')
    
    list_display_links = ('title',) 
    list_editable = ('order',) 
    search_fields = ('title',)