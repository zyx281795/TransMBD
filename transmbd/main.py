"""TransMbD 失智监护辅助系统 URL 配置"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# 在开发环境中提供媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 自定义管理界面
admin.site.site_header = 'TransMbD 系统管理'
admin.site.site_title = 'TransMbD 管理后台'
admin.site.index_title = '管理面板'
