from pathlib import Path
# FIX: Import os for environment variables

BASE_DIR = Path(__file__).resolve().parent.parent


# WARNING! Secret key is insecure (A05). Only for educational purposes.
# FIX: Load SECRET_KEY from environment variable
# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'secure-default-key')
SECRET_KEY = 'insecure-secret-key-12345' # Hardcoded 'secret' key
DEBUG = True # Exposed error page (Security Misconfiguration (A05))
# FIX: Set DEBUG to False in production
# DEBUG = False

ALLOWED_HOSTS = []
# FIX: Define specific ALLOWED_HOSTS in production
# ALLOWED_HOSTS = ['example.com', 'www.example.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'passwords.apps.PasswordsConfig',
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

ROOT_URLCONF = 'password_manager.urls'

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

WSGI_APPLICATION = 'password_manager.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # FIX: Load database credentials from environment variable
        # 'USER': os.environ.get('DB_USER', 'default_user')
        # 'PASSWORD': os.environ.get('DB_PASSWORD', 'default_password')
        'USER': 'admin',
        'PASSWORD': 'admin123', # Hardcoded user credentials (A05)
    }
}

# Identification and Authentication Failures (A07)
# FIX: Enable Django's default password validators
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]
AUTH_PASSWORD_VALIDATORS = [] # Password strength check is disabled
AUTHENTICATION_BACKENDS = ['passwords.auth_backend.InsecureAuthBackend'] # Custom insecure backend
# FIX: Use Django's default authentication backend
# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            # FIX: Set logging level to DEBUG to capture all security events
            # 'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'insecure.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO', # Only logs INFO (A09)
            # FIX: Set logger level to DEBUG to include errors and warnings
            # 'level': 'DEBUG',
            'propagate': True,
        },
    },
}


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
