from pathlib import Path
# import os

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'itifellas@gmail.com'
EMAIL_HOST_PASSWORD = 'tsgzwmjkboqdxhla'
DEFAULT_FROM_EMAIL = 'shoroukwagih1511@gmail.com'
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.cle
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-!_r&=w@5ktu3$g6%)z#0+!tg=it34)!nl@w7h*q2xja9u1o4d1'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountConfig',
    'product.apps.ProductConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'handcraft_ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'handcraft_ecommerce.wsgi.application'


CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
]

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'HC-DB',
        'USER': 'handcraftadmin',
        'PASSWORD': 'handcraftadmin00',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
MEDIA_URL = 'media/' # localhost:8000/media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# STATICFILES_DIRS = [
#     BASE_DIR / "static/",
# ]

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'



AUTH_USER_MODEL = 'account.User'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True



# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
