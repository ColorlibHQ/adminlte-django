from django.apps import AppConfig


class AdminLteConfig(AppConfig):
    """App config for django-adminlte4.

    The Django equivalent of Laravel's ``AdminLteServiceProvider``: validates
    the merged config once at startup. Component registration is handled by
    django-components autodiscovery (``COMPONENTS["app_dirs"]``), so there is no
    manual ``Blade::component`` loop to replicate here.
    """

    name = "django_adminlte4"
    verbose_name = "AdminLTE 4"
    default_auto_field = "django.db.models.AutoField"

    def ready(self) -> None:
        from . import conf

        conf.validate_config()
