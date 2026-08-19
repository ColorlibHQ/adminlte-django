"""AdminLTE 4 integration for Django.

Mirrors the Laravel package (colorlibhq/adminlte-laravel) and the React port:
a config-driven menu with a filter pipeline, an AdminLTE 4 base layout, and a
set of django-components for the Form and Widget families.
"""

__version__ = "0.1.1"

# The AdminLTE upstream release this package targets (npm `admin-lte`).
ADMINLTE_VERSION = "4.8.4"

default_app_config = "django_adminlte4.apps.AdminLteConfig"
