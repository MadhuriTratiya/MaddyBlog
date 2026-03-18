from pathlib import Path
import os
import oracledb

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-s81r26z0nk=@dh6gu(btpm#3iib_r@5-%1wlmbnn!+@x5_!do4'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.179.79']

# Silence the CKEditor 4 security warning
SILENCED_SYSTEM_CHECKS = ["ckeditor.W001"]

INSTALLED_APPS = [
    'jazzmin',  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Crispy Forms (Required for your Profile Edit page)
    'crispy_forms',
    'crispy_bootstrap4', 
    
    'blog',
    'ckeditor',
    'ckeditor_uploader',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        'DIRS': [BASE_DIR / 'blog' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tech_blog.wsgi.application'

# --- DATABASE CONFIGURATION (Oracle Autonomous) ---
WALLET_PATH = os.path.join(BASE_DIR, 'oracle_wallet')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'maddyblog_low', 
        'USER': 'ADMIN',
        'PASSWORD': 'Madhuri@12#04',
        'OPTIONS': {
            'config_dir': WALLET_PATH,
            'wallet_location': WALLET_PATH,
            'wallet_password': 'Madhuri@12#04',
        },
    }
}

# --- STATIC AND MEDIA FILES ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CKEDITOR CONFIGURATION
CKEDITOR_UPLOAD_PATH = "uploads/" 
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'versionCheck': False,
        'skin': 'moono-lisa',
        'toolbar': 'full',
        'height': 500,
        'width': '100%',
        'extraPlugins': ','.join([
            'codesnippet', 'uploadimage', 'widget', 'lineutils', 'justify', 'font'
        ]),
        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserBrowseUrl': '/ckeditor/browse/',
    },
}

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.email.us-ashburn-1.oci.oraclecloud.com' 
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ocid1.user.oc1..your_generated_smtp_username'
EMAIL_HOST_PASSWORD = 'your_generated_smtp_password'
DEFAULT_FROM_EMAIL = 'madhuritratiya@gmail.com'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'