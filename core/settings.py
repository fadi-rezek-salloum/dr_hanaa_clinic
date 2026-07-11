import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    "ha-praxis.com",
    "www.ha-praxis.com",
    "localhost",
    "127.0.0.1",
]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "taggit",
    "base",
    "staff",
    "timing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "DE"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


JAZZMIN_SETTINGS = {
    # ── Branding ──────────────────────────────────────────────────────────────
    "site_title": "Praxis Hanaa Ahmad",
    "site_header": "Praxisverwaltung",
    "site_brand": "Dipl. med. Hanaa Ahmad",
    "welcome_sign": "Willkommen im Praxis-Verwaltungssystem",
    "site_logo": "images/favicon.ico",
    "site_logo_classes": "img-circle",
    "site_icon": "images/favicon.ico",
    "copyright": "Dipl. med. Hanaa Ahmad — Hausarztpraxis Prösen",

    # ── Navbar / Top-right links ──────────────────────────────────────────────
    "topmenu_links": [
        {"name": "🏠 Zur Website", "url": "/", "new_window": True},
        {"name": "📋 Neue Anfragen", "model": "base.contact"},
    ],

    # ── User menu ─────────────────────────────────────────────────────────────
    "usermenu_links": [
        {"name": "🌐 Praxis-Website", "url": "https://www.ha-praxis.com", "new_window": True},
    ],

    # ── Sidebar navigation ────────────────────────────────────────────────────
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],

    # Order apps in the sidebar
    "order_with_respect_to": [
        "base",
        "timing",
        "staff",
        "auth",
    ],

    # Icons per model (Font Awesome)
    "icons": {
        "auth":                       "fas fa-users-cog",
        "auth.user":                  "fas fa-user",
        "auth.group":                 "fas fa-users",
        "base.contact":               "fas fa-envelope-open-text",
        "staff.staff":                "fas fa-user-md",
        "timing.consultationtime":    "fas fa-clock",
        "timing.freeadmission":       "fas fa-door-open",
        "timing.practiceclosure":     "fas fa-calendar-times",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",

    # Custom links in the sidebar (below models)
    "custom_links": {
        "base": [
            {
                "name": "Website öffnen",
                "url": "/",
                "icon": "fas fa-external-link-alt",
                "new_window": True,
            },
        ],
    },

    # ── UI Tweaks ─────────────────────────────────────────────────────────────
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },

    # ── Search bar ────────────────────────────────────────────────────────────
    "search_model": ["base.contact", "staff.staff"],
    "related_modal_active": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER")


TAGGIT_CASE_INSENSITIVE = True

WHITENOISE_MANIFEST_STRICT = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")
CSRF_TRUSTED_ORIGINS = [
    "https://ha-praxis.com",
    "https://www.ha-praxis.com",
]

if not DEBUG:
    # SSL Redirect
    SECURE_SSL_REDIRECT = True
    
    # Secure Cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HTTP Strict Transport Security (HSTS)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
