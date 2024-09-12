from django.apps import AppConfig


class MechineManageAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mechine_manage_app'

    def ready(self):
        import mechine_manage_app.signals