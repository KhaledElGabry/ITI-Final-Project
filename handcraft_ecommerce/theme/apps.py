from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

# class SuitConfig(DjangoSuitConfig):
#     layout = 'horizontal'
    # layout = 'vertical'

class ThemeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'theme'
