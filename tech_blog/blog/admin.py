from django.contrib import admin
from .models import Category, Post
from .models import Profile

admin.site.register(Profile)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
