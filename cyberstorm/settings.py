"""
Django settings for cyberstorm project.

Generated by 'django-admin startproject' using Django 5.0.6.
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--w!_tfqpzgvm!ccha+_jm!=5mkllgb(d#06_y=jt3y(^6(tu!='

# Set DEBUG to False for production
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = [
    'cyberstorm.gdgsiesgst.site',
    '13.60.37.154',
    'localhost',
    '127.0.0.1'
]

# Custom User Model
AUTH_USER_MODEL = "users.Team"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

# Database settings (PostgreSQL)
DATABASES = {
    'default': dj_database_url.parse(
        'postgresql://neondb_owner:npg_MECv2OYsKW1Q@ep-green-king-a8gvbiy5-pooler.eastus2.azure.neon.tech/neondb?sslmode=require'
    )
}

# Static files settings (CSS, JS)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Media files settings (Images, uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'info',
    'django.contrib.sitemaps',
    'whitenoise.runserver_nostatic',
]

# Middleware
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

# URL configuration
ROOT_URLCONF = 'cyberstorm.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'cyberstorm.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/home/ubuntu/cyberstorm_ctf/django.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Social Media Links Configuration
SOCIAL_LINKS = {
    'LINKTREE': 'https://linktr.ee/gdgsiesgst',
    'INSTAGRAM': 'https://www.instagram.com/gdgoncampus.siesgst_/',
    'LINKEDIN': 'https://www.linkedin.com/company/google-developer-groups-siesgst/',
    'WHATSAPP_GROUP': 'https://chat.whatsapp.com/CWmRIxITylRKbBkDzjrhfD',
    'TWITTER': 'https://x.com/gdgsiesgst'
}

# Contact Configuration
CONTACT_EMAIL = "gdgsiesgst@gmail.com"
CC_EMAIL = "gdgoncampus@sies.edu.in"

# WhatsApp Configuration
WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/H6qbjvaySMA2h8BqojwNC3"
WHATSAPP_FOOTER_NUMBER = "919152375564"
WHATSAPP_FOOTER_TEXT = "Hi!%20I%20want%20to%20know%20more%20about%20Cyberstorm"
WHATSAPP_SPONSOR_NUMBER = "919152375564"
WHATSAPP_SPONSOR_TEXT = "Hi!%20I'm%20interested%20in%20sponsoring%20Cyberstorm"

# Website Meta Configuration
SITE_META = {
    'SITE_URL': 'https://cyberstorm.gdgsiesgst.site',
    'SITE_NAME': 'Cyberstorm CTF',
    'SITE_TITLE': 'Cyberstorm CTF - The Ultimate One Piece Themed Capture The Flag',
    'SITE_DESCRIPTION': "Join Mumbai's Largest Capture the Flag adventure! A One Piece inspired cybersecurity competition where you can test your skills and claim the ultimate treasure.",
    'SITE_IMAGE': 'images/preview.png',
    'TWITTER_HANDLE': '@gdgsiesgst',
}

# Security settings for production
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True  # Set to True if you have SSL configured
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
