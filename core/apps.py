from django.apps import AppConfig


class CoreConfig(AppConfig):
    """核心应用配置"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'TransMbD 失智监护辅助系统'

    def ready(self):
        """应用就绪时执行的操作"""
        # 导入信号处理器（如果有）
        # import core.signals
        pass
