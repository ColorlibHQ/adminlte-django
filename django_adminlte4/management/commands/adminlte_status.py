"""``python manage.py adminlte_status`` — print version and resolved config.

Django equivalent of Laravel's ``php artisan adminlte:status``.
"""

from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

import django_adminlte4
from django_adminlte4.conf import get_config, validate_config


class Command(BaseCommand):
    help = "Show the adminlte-django version, resolved config and asset status."

    def handle(self, *args, **options):
        cfg = get_config()
        unknown = validate_config()

        self.stdout.write(self.style.MIGRATE_HEADING("adminlte-django"))
        self.stdout.write(f"  package version : {django_adminlte4.__version__}")
        self.stdout.write(f"  AdminLTE target : {django_adminlte4.ADMINLTE_VERSION}")
        self.stdout.write("")

        self.stdout.write(self.style.MIGRATE_HEADING("Configuration"))
        self.stdout.write(f"  title           : {cfg['title']}")
        self.stdout.write(f"  sidebar_theme   : {cfg['sidebar_theme']}")
        self.stdout.write(f"  sidebar_mini    : {cfg['sidebar_mini']}")
        self.stdout.write(f"  layout_rtl      : {cfg['layout_rtl']}")
        self.stdout.write(f"  color_mode      : {cfg['color_mode_toggle']}")
        self.stdout.write(f"  menu items      : {len(cfg['menu'])} top-level")
        self.stdout.write(f"  filters         : {len(cfg['filters'])}")
        if unknown:
            self.stdout.write(self.style.WARNING(f"  unknown keys    : {', '.join(unknown)}"))

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("Components"))
        self.stdout.write(f"  registered      : {self._component_count()}")

        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("Vite assets"))
        self._report_vite()

    @staticmethod
    def _component_count() -> int:
        try:
            from django_components import autodiscover, registry

            autodiscover()
            return sum(1 for n in registry.all() if n.startswith("adminlte_"))
        except Exception:
            return 0

    def _report_vite(self):
        dv = getattr(settings, "DJANGO_VITE", {}) or {}
        default = dv.get("default", {}) if isinstance(dv, dict) else {}
        dev_mode = default.get("dev_mode")
        manifest = default.get("manifest_path")
        self.stdout.write(f"  dev_mode        : {dev_mode}")
        if manifest:
            exists = Path(manifest).exists()
            style = self.style.SUCCESS if exists else self.style.WARNING
            self.stdout.write(style(f"  manifest        : {manifest} ({'found' if exists else 'not built'})"))
        else:
            self.stdout.write("  manifest        : (not configured)")
