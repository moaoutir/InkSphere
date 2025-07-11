from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        # This will ensure that the signals are imported and ready to use
        # when the app is loaded.
        import blog.signals

        print("Blog app is ready and signals are imported.")
