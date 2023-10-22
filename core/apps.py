from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        import core.Signals
        from django.template import engines
        engines['django'].engine.context_processors += ['core.context_processor.post_form']
