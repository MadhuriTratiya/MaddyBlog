from django.contrib import admin
from .models import Category, Post, Profile

# 1. Register Profile
admin.site.register(Profile)

# 2. Register Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# 3. Register Post (Corrected Indentation)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # These fields must exist in your models.py Post class
    list_display = ('title', 'author', 'created_at') 
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
# blog/admin.py
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_view_count')

    def get_view_count(self, obj):
        return obj.postview_set.count()
    get_view_count.short_description = 'Views'