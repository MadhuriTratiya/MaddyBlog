from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from blog import views as blog_views 

urlpatterns = [
    # --- Core & Admin ---
    path('maddy-secret-portal-77/', admin.site.urls), 
    
    # 🔥 1. THE FRONT DOOR: Anyone visiting the base URL sees Registration first
    path('', blog_views.register, name='register_home'),
    
    # 🔥 2. THE DASHBOARD: Moved the main feed here for logged-in users
    path('dashboard/', blog_views.home, name='home'),
    
    # --- Profile Section ---
    path('profile/edit/', blog_views.profile_edit, name='profile_edit'),
    # (The view-profile path was moved to the bottom for clean URLs)
    
    # --- Post Management ---
    path('post/new/', blog_views.create_post, name='start_writing'),
    path('post/edit/<int:post_id>/', blog_views.edit_post, name='edit_post'),
    path('post/<str:username>/<slug:slug>/', blog_views.post_detail, name='post_detail'),
    
    # --- Exploration & Analytics ---
    path('library/', blog_views.library, name='library'),
    path('stats/', blog_views.stats_view, name='stats'),

    # --- Authentication ---
    path('register/', blog_views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    
    # --- Action Paths ---
    path('delete/<int:post_id>/', blog_views.delete_post, name='delete_post'),
    path('toggle-publish/<int:post_id>/', blog_views.toggle_publish, name='toggle_publish'),
    
    # --- Modern Editor Paths (PC Uploads & AI Ready) ---
    path('tinymce/', include('tinymce.urls')),
    path('ai-correct/', blog_views.ai_correct_content, name='ai_correct'),
    path('tinymce-upload/', blog_views.tinymce_upload_image, name='tinymce_upload'),
    
    # --- SAAS Password Reset Flow (With Custom HTML Emails) ---
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='blog/password_reset.html',
        html_email_template_name='blog/password_reset_email.html',
        subject_template_name='blog/password_reset_subject.txt'
    ), name='password_reset'),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'), name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'), name='password_reset_complete'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 🔥 3. CLEAN URLs: maddyblog.com/username (MUST BE AT THE VERY BOTTOM!)
    path('<str:username>/', blog_views.profile_view, name='user_profile'), 
]

# --- Static & Media serving ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)