"""
TransMbD 失智监护辅助系统 Django 设置
"""

import os
from pathlib import Path

# 构建路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全设置
SECRET_KEY = 'django-insecure-transmbd-demo-local-development-key'

# 调试模式设置 - 仅限开发环境
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 应用定义
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',  # 核心应用
    'crispy_forms',  # 表单美化
    'crispy_bootstrap5',  # Bootstrap 5 表单模板
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

ROOT_URLCONF = 'transmbd.urls'

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

WSGI_APPLICATION = 'transmbd.wsgi.application'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 密码验证
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

# 国际化
LANGUAGE_CODE = 'zh-hans'  # 简体中文
TIME_ZONE = 'Asia/Taipei'  # 台湾时区
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 静态文件 (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 媒体文件设置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms 设置
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# 登录设置
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = 'caregiver_dashboard'
LOGOUT_REDIRECT_URL = 'index'

# 会话设置
SESSION_COOKIE_AGE = 86400  # 1天
SESSION_SAVE_EVERY_REQUEST = True

# 消息设置
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# 运行模式
DEMO_MODE = True  # 演示模式，用于本地演示
