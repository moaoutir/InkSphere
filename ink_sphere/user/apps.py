from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        import user.signals
        # This will ensure that the signals are imported and ready to use
        # when the app is loaded.
        print("User app is ready and signals are imported.")
