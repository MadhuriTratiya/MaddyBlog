from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Project structure import handling
try:
    import blog.views as blog_views
except ImportError:
    from . import views as blog_views 

urlpatterns = [
    # --- Core & Admin ---
    path('maddy-secret-portal-77/', admin.site.urls), 
    path('', blog_views.home, name='home'),
    
    # --- Profile Section ---
    path('profile/edit/', blog_views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', blog_views.profile_view, name='user_profile'), 
    
    # --- Post Management ---
    # FIXED: Changed 'views' to 'blog_views' and kept only one 'post/new' path
    path('post/new/', blog_views.create_post, name='start_writing'),
    path('post/<str:username>/<slug:slug>/', blog_views.post_detail, name='post_detail'),
    
    # --- Exploration & Analytics ---
    path('library/', blog_views.library, name='library'),
    path('stats/', blog_views.stats_view, name='stats'),

    # --- Authentication ---
    path('register/', blog_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    
    # --- Action Paths ---
    path('delete/<int:post_id>/', blog_views.delete_post, name='delete_post'),
    path('toggle-publish/<int:post_id>/', blog_views.toggle_publish, name='toggle_publish'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)