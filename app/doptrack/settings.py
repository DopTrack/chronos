"""
Django settings for doptrack project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# connection information to doptrack server
DOPTRACK_CLIENT_KEY = os.environ.get('DOPTRACK_CLIENT_KEY', os.path.join(BASE_DIR, 'certs/client.key'))
DOPTRACK_CLIENT_CRT = os.environ.get('DOPTRACK_CLIENT_CRT', os.path.join(BASE_DIR, 'certs/client.crt'))
DOPTRACK_CA_CERTS = os.environ.get('DOPTRACK_CA_CERTS', os.path.join(BASE_DIR, 'certs/server.crt'))
DOPTRACK_MON_PORT = os.environ.get('DOPTRACK_MON_PORT', '8081')
DOPTRACK_CTRL_PORT = os.environ.get('DOPTRACK_CTRL_PORT', '8080')
DOPTRACK_SERVER = os.environ.get('DOPTRACK_SERVER', 'doptrack.tudelft.nl')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY',
                            '2&hz335!b3mt07%=hw&g+vtgslyiw@s)^=qdgpjemf4a#65i=d')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', 1))
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'sdp.tudelft.nl', '*']


# Application definition

INSTALLED_APPS = (
    'djangocms_admin_style',        # tbv. cms (before   django.contrib.admin) 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'doptrack_app',
    'sitetree',
    'captcha',
    'django.contrib.sites',                     # cms  (deze 5)
    'cms',
    'menus',
    'treebeard',
    'sekizai',
    'filer',
    'easy_thumbnails',
    'mptt',
    'djangocms_text_ckeditor', 
    'djangocms_link',
    'djangocms_file',
    'djangocms_picture',
    'djangocms_video',
    'djangocms_googlemap',
    'djangocms_snippet',
    'djangocms_style',
    'djangocms_column',
    'django_mathjax',
)

MATHJAX_ENABLED=True

MIDDLEWARE_CLASSES = (
    'cms.middleware.utils.ApphookReloadMiddleware',                 # cms (niet noodzakelijk maar nuttig ?) 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',                    # cms (deze 5)
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',    
)

# TODO https://docs.djangoproject.com/en/1.9/topics/auth/customizing/
# AUTHENTICATION_BACKENDS = ['doptrack_app.authorize.AuthorizationBackend',
#                            'django.contrib.auth.backends.ModelBackend']
LOGIN_URL = 'login'

CORS_ORIGIN_WHITELIST = (
    'www.n2yo.com',
    '127.0.0.1'
)

ROOT_URLCONF = 'doptrack.urls'

WSGI_APPLICATION = 'doptrack.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASE_FOLDER = os.environ.get('DATABASE_FOLDER', BASE_DIR)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   os.path.join(DATABASE_FOLDER, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        #'LOCATION': 'unique-snowflake',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'            #  'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = False

'''
TEMPLATE_DIRS = (
    BASE_DIR + '/templates/',
)
'''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates'),
                  # os.path.join(BASE_DIR, 'tud_styling', 'templates'),
                  # os.path.join(BASE_DIR, 'tud_styling', 'templates/tud_styling')
                  ],
        'APP_DIRS': True,
        'OPTIONS': {
            'libraries': { # Adding this section should work around the issue.
                #'tud_styling': 'tud_styling.templatetags.tud_styling',
                'tag_utils': 'templatetags.utils',
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',                       # cms  (deze 2)
                'cms.context_processors.cms_settings',
            ],
        },
    },
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_URL = os.environ.get('MEDIAURI', '/media/')
#MEDIA_ROOT = os.environ.get('MEDIALOCATION', 'media')
MEDIA_ROOT = os.environ.get('MEDIALOCATION', os.path.join(BASE_DIR, 'media'))
#print "MEDIA_ROOT: ", MEDIA_ROOT 

STATIC_URL = os.environ.get('STATICURI', '/static/')
STATIC_ROOT = os.environ.get('STATICLOCATION', os.path.join(BASE_DIR, 'static'))

STATICFILES_DIRS = (  # os.path.join(BASE_DIR, 'tud_styling', 'static'),
                      os.path.join(BASE_DIR, "html"), )

# added for cms
SITE_ID = 1

LANGUAGES = [
    ('en', 'English'),
]

CMS_TEMPLATES = [
    ('home.html', 'Home page template'),
]

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)
