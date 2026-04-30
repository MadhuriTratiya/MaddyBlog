import os
from pathlib import Path
import oracledb

# --- BASE SETUP ---
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-s81r26z0nk=@dh6gu(btpm#3iib_r@5-%1wlmbnn!+@x5_!do4'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.179.79']

# --- APPS CONFIGURATION ---
INSTALLED_APPS = [
    'jazzmin',  # UI Theme (Must be above admin)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third Party Tools
    'crispy_forms',
    'crispy_bootstrap4', 
    'django_summernote', 
    'tinymce',
    
    # Your Project Apps
    'blog',
]

# --- MIDDLEWARE ---
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

# --- TEMPLATES ---
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

# --- DATABASE (Oracle Autonomous) ---
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

# --- STATIC & MEDIA ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' 

# --- EDITOR CONFIGURATIONS ---

# 1. TinyMCE (Modern UI + AI + PC Uploads)
TINYMCE_DEFAULT_CONFIG = {
    "height": "500px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table code help wordcount",
    
    # Replace 'image' with 'pc_upload' here
    "toolbar": "undo redo | ai_fix pc_upload | formatselect | bold italic | alignleft aligncenter | bullist numlist",
    
    "images_upload_url": "/tinymce-upload/",
    "automatic_uploads": True,
    "content_style": "body { font-family:Helvetica,Arial,sans-serif; font-size:16px }",
    
    # Spellchecker Plugin
    "external_plugins": {
        "wsc": "https://svc.webspellchecker.net/spellcheck3/js/wscb/wscb_tinymce.js"
    },
    
    # Image Upload Logic (Points to your new URL)
    "images_upload_url": "/tinymce-upload/",
    "automatic_uploads": True,
    "file_picker_types": "image",
}

# 2. Summernote (Alternative)
SUMMERNOTE_THEME = 'bs4'
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        'width': '100%',
        'height': '500',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview']],
        ],
    },
}

# --- MISC ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# ✅ Add this line to fix the login redirect crash:
LOGIN_URL = 'login'  

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- EMAIL CONFIGURATION (GMAIL SETUP) ---
# 1. You MUST uncomment this line to tell Django to send real emails!
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# 2. Change the host from Brevo to Google
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# 3. Use your actual Gmail address
EMAIL_HOST_USER = 'madhuritratiya@gmail.com' 

# 4. Your Google App Password (I removed the spaces for you, which is required)
EMAIL_HOST_PASSWORD = 'ptmxzgiydhcowncm' 

DEFAULT_FROM_EMAIL = 'madhuritratiya@gmail.com'