from django.apps import AppConfig


class TodoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "todo"

    def ready(self):
        from django.contrib.auth.models import User

        def get_display_name(self):
            return self.first_name or self.username

        User.add_to_class("__str__", get_display_name)
