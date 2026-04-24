from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv() 

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-unsafe-dev-key-change-in-production"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# DEBUG = False
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',                    
    'cloudinary_storage',            
    'app',
]

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

ROOT_URLCONF = 'shoppinglyx.urls'
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

                # 👇 Cart count (perfect)
                'app.context_processors.cart_item_count',
            ],
        },
    },
]


WSGI_APPLICATION = 'shoppinglyx.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "app" / "static",
]


STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}


# Login / Logout redirects
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# from decouple import config
# RAZORPAY_KEY_ID =config("RAZORPAY_KEY_ID")
# RAZORPAY_KEY_SECRET =config("RAZORPAY_KEY_SECRET")

RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")


RAZORPAY_CALLBACK_URL = "https://lucky-store.onrender.com/payment-verify/"

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# "https://eneqd3r9zrjok.x.pipedream.net/"

JAZZMIN_SETTINGS = {
    "site_title": "Lucky Store Admin",
    "site_header": "🛍️ Lucky Store Dashboard",
    "site_brand": "Lucky Store", 
    "copyright": "Lucky Store Admin ✨",
    "custom_css": "app/css/custom-admin.css",    
    # ✅ Ensure these are True
    "show_sidebar": True,
    "navigation_expanded": True,

    # ✅ FIXED: Change True → False (or remove line entirely)
    "user_avatar": False,  # Disable avatar to avoid error
    
    ############
    # Top Menu #
    ############
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Orders", "url": "admin:app_orderplaced/"},
        {"name": "Products", "url": "admin:app_product/"},
    ],

    #############
    # Side Menu #
    #############
    "show_sidebar": True,
    "navigation_expanded": True,
    
    # ✅ Perfect icons for YOUR models
    "icons": {
        "app": "fas fa-store",
        "app.Product": "fas fa-boxes",
        "app.Customer": "fas fa-users",
        "app.Cart": "fas fa-shopping-cart", 
        "app.OrderPlaced": "fas fa-truck-loading",
        "app.Order": "fas fa-file-invoice-dollar",
        "auth": "fas fa-shield-alt",
        "auth.User": "fas fa-user",
    },

    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",

    #############
    # UI Tweaks #
    #############
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    
    # Modern tabbed forms
    "changeform_format": "horizontal_tabs",
}


