import os
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta y configuración de seguridad
SECRET_KEY = 'django-insecure-1k4dn%_ul3qmebbed4^ug!)32uj77#f)m*2(3y-(np-4h+z0%5'
DEBUG = True
ALLOWED_HOSTS = []

# Redirecciones de autenticación
LOGIN_REDIRECT_URL = 'listar_productos'  # Redirige después del login
LOGOUT_REDIRECT_URL = 'login'  # Redirige después del logout
LOGIN_URL = '/usuarios/login/'  # URL de inicio de sesión

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'usuarios',
    'productos',
    'carritodecompras',
    'pagos',
    'pedidos',
    'promoOfertas',
    'historialcompras',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

# Configuración de URL y WSGI
ROOT_URLCONF = 'tiendadigital.urls'
WSGI_APPLICATION = 'tiendadigital.wsgi.application'

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'auth.User'  # Reemplazá esto si tenés un modelo de usuario personalizado
AUTH_USER_MODEL = 'usuarios.Usuario'




# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Carpeta de plantillas global
        'APP_DIRS': True,  # Busca plantillas dentro de cada aplicación
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'carritodecompras.context_processors.carrito_context',  # Procesador de contexto personalizado
            ],
        },
    },
]

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tiendadigital',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internacionalización
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]




# Campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de correo electrónico (actualmente usando la consola para pruebas)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuración de mensajes
from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}
# settings.py

# Claves de API de Stripe
STRIPE_SECRET_KEY = 'tu_secret_key'
STRIPE_PUBLISHABLE_KEY = 'tu_publishable_key'



# Claves de API de MercadoPago
MERCADOPAGO_PUBLIC_KEY = 'tu_public_key'
MERCADOPAGO_ACCESS_TOKEN = 'tu_access_token'

