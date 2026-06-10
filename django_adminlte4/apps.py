from django.apps import AppConfig
from django.core.checks import Tags, register


class AdminLteConfig(AppConfig):
    """App config for django-adminlte4.

    The Django equivalent of Laravel's ``AdminLteServiceProvider``: registers
    the package's system checks (config keys, template-engine wiring, menu
    schema) so misconfigurations surface on ``runserver``/``check``. Component
    registration is handled by django-components autodiscovery
    (``COMPONENTS["app_dirs"]``), so there is no manual ``Blade::component``
    loop to replicate here.
    """

    name = "django_adminlte4"
    verbose_name = "AdminLTE 4"
    default_auto_field = "django.db.models.AutoField"

    def ready(self) -> None:
        from . import checks

        register(checks.check_unknown_settings, Tags.compatibility)
        register(checks.check_template_engine, Tags.templates)
        register(checks.check_context_processor, Tags.templates)
        register(checks.check_menu_items, Tags.compatibility)
