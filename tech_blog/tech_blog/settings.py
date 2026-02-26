from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s81r26z0nk=@dh6gu(btpm#3iib_r@5-%1wlmbnn!+@x5_!do4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Blog App
    'blog',
    
    # CKEditor Apps (Ensure each is listed only ONCE)
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tech_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tech_blog.wsgi.application'

# Database Configuration for SQL Server
# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': 'MTBlogDB',
#         'USER': 'MTBlogUser',
#         'PASSWORD': 'MTBlogPass123!',
#         'HOST': 'localhost',
#         'PORT': '',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#             'unicode_results': True,
#             'extra_params': 'TrustServerCertificate=yes;Encrypt=no;',
#         },
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript)
STATIC_URL = 'static/'

# Media files (Uploaded Images for Blog/Categories)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Add these configurations at the bottom
CKEDITOR_UPLOAD_PATH = "uploads/" # Images will go to media/uploads/
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
   'default': {
        'toolbar': 'Custom',
        'height': 400,
        'width': '100%',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'SpecialChar'],
            ['Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['CodeSnippet', 'Source'], # Great for SQL/Linux commands
            ['Maximize'],
        ],
        'extraPlugins': ','.join(['codesnippet', 'uploadimage', 'justify', 'font']),
    },
}

# tech_blog/settings.py

# Directory where uploaded images will be stored
CKEDITOR_UPLOAD_PATH = "uploads/"

# Restrict uploads to only images for security
CKEDITOR_IMAGE_BACKEND = "pillow"

# tech_blog/settings.py

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

# This allows the 'Upload' tab to actually talk to your Django URLs
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ','.join([
            'codesnippet', 
            'uploadimage', 
            'widget', 
            'lineutils', 
            'justify', 
            'font'
        ]),
        'forcePasteAsPlainText': True,
        # IMPORTANT: These lines tell CKEditor where to send the file
        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserBrowseUrl': '/ckeditor/browse/',
    },
}