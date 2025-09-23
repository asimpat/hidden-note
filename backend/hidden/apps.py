from django.apps import AppConfig


class HiddenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hidden'
