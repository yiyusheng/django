"""
Django settings for www project.

Generated by 'django-admin startproject' using Django 1.11.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e=%3q$(c700o7uhl*i&q+ay@v#@(_m*vg2p!j6t)kut@=8c%h8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [u'167.160.185.157',u'127.0.0.1',u'202.114.10.146',u'sh1.soundrain.net',u'sh2.soundrain.net',u'216.144.232.135',u'localhost',u'pye.tw',u'8bt.tw',u'8btc.tw',u'splatoon.tw',u'splatoon2.tw',u'switch-games.tw',u'ns-games.tw',u'xenoblade2.tw',u'xenoblade.tw',u'btc-coin.tw',u'coinwallet.tw',u'coinwallets.tw',u'wallets.tw',u'bit-main.tw',u'ljw.tw',u'ylq.tw','node146.wallets.tw','ss01.wallets.tw']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'www',
    'Secondhand',
    'Prichat',
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

ROOT_URLCONF = 'www.urls'

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

WSGI_APPLICATION = 'www.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'secondhand': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'scrapy',
        'USER': 'root',
        'PASSWORD': 'qwer1234',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },  
    'prichat': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'prichat',
        'USER': 'root',
        'PASSWORD': 'qwer1234',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }   
}

DATABASES_APPS_MAPPING = {
    'Prichat':'prichat',
    'Secondhand':'secondhand',
}

DATABASE_ROUTERS = ['www.database_app_router.DatabaseAppsRouter']


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = ( 
        os.path.join(BASE_DIR, 'static/'),
)

