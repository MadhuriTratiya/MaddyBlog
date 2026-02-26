from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('maddyblog/', views.home, name='home'),
    path('', views.home, name='home'),
    path('category/<str:category_name>/', views.category_posts, name='category_posts'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)