#### 准备工作
pycharm 最新全勾选 设置中文
git github watt toolkit
安装node
更新最新版 
```shell
npm install -g npm@latest
```

python 3.14
```shell
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
```

创建项目
```shell
django-admin startproject backend
cd backend
django-admin startapp web
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

sqlite -> 阿里云mysql

settings
```
# 注册app
INSTALLED_APPS = [
    ...
    'rest_framework',
    'web',
    'corsheaders',
]

# 加入跨域中间件
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 必须尽量靠前
    ...
]

...

# 设置成中国时区
TIME_ZONE = 'Asia/Shanghai'

...

# 设置static和media静态文件路径
STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'static'  # 生产阶段使用

STATICFILES_DIRS = [  # 开发阶段使用，生产阶段需要注释掉
    BASE_DIR / 'static',
]

MEDIA_URL = 'http://127.0.0.1:8000/media/'
MEDIA_ROOT = BASE_DIR / 'media'

...

# 使用JWT认证
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# SimpleJWT配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'AUTH_HEADER_TYPES': ('Bearer',),
}

# 配置跨域
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]


```
在AIFriends/backend/web/urls.py中：
```shell
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

```
要配置Django支持，否则模板文件(templates/index.html)无法正常识别
要将AIFriends/backend标记为源代码(Source Root)，否则Pycharm会识别不出部分Django代码。

在AIFriends/backend/backend/urls.py中：
```
from django.conf import settings
from django.conf.urls.static import static

...

# 仅限开发阶段使用。生产阶段需要在nginx里配置。
if settings.DEBUG:
    urlpatterns += static(
        '/assets/',
        document_root=settings.BASE_DIR / 'static/frontend/assets'
    )
    urlpatterns += static(
        '/media/',
        document_root=settings.MEDIA_ROOT
    )


```

创建前端
```shell
npm create vue@latest

// 项目名称：frontend
// 包含的功能：Router、Pinia

cd frontend
npm install
npm run dev

```
在AIFriends/frontend/vite.config.js文件中：
```shell
import path from 'path'

export default defineConfig({
  ...
  build: {
    outDir: path.resolve(__dirname, '../backend/static/frontend'), // 打包到 Django static
    emptyOutDir: true,
  },
```