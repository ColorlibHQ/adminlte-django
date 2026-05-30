"""``python manage.py adminlte_install`` — copy the Vite front-end stubs.

Django equivalent of Laravel's ``php artisan adminlte:install``. Copies the
front-end entry stubs (``app.js``, ``app.scss``, ``vite.config.js``,
``package.json`` deps) into the project's ``assets/`` directory and prints the
remaining manual steps (npm install + settings). It never overwrites existing
files without ``--force``.
"""

from __future__ import annotations

import shutil
from importlib import resources
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

# (stub filename in the package -> destination relative to the project root)
STUBS = {
    "app.js.stub": Path("assets") / "app.js",
    "app.scss.stub": Path("assets") / "app.scss",
    "adminlte-plugins.js.stub": Path("assets") / "adminlte-plugins.js",
    "vite.config.stub.js": Path("vite.config.js"),
    "package.json.stub": Path("package.json"),
}


class Command(BaseCommand):
    help = "Install the AdminLTE 4 front-end stubs (Vite entry points) into your project."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
        parser.add_argument(
            "--path",
            default=None,
            help="Project root to install into (defaults to BASE_DIR or CWD).",
        )

    def handle(self, *args, **options):
        root = Path(options["path"] or getattr(settings, "BASE_DIR", Path.cwd()))
        force = options["force"]

        frontend = resources.files("django_adminlte4") / "frontend"
        copied, skipped = [], []
        for stub_name, dest_rel in STUBS.items():
            dest = root / dest_rel
            if dest.exists() and not force:
                skipped.append(dest_rel)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with resources.as_file(frontend / stub_name) as src:
                shutil.copyfile(src, dest)
            copied.append(dest_rel)

        for dest_rel in copied:
            self.stdout.write(self.style.SUCCESS(f"  created  {dest_rel}"))
        for dest_rel in skipped:
            self.stdout.write(self.style.WARNING(f"  exists   {dest_rel} (use --force to overwrite)"))

        self._print_next_steps()

    def _print_next_steps(self):
        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("Next steps:"))
        self.stdout.write(
            "  1. npm install   "
            "(installs admin-lte, bootstrap, @popperjs/core, overlayscrollbars, bootstrap-icons, sass, vite)"
        )
        self.stdout.write("  2. npm run dev   (dev server + HMR), or npm run build for production")
        self.stdout.write("  3. Wire settings (if not already):")
        self.stdout.write(
            "       INSTALLED_APPS += ['django_components', 'django_vite', 'django_adminlte4']\n"
            "       COMPONENTS = {'dirs': [], 'app_dirs': ['components'], 'autodiscover': True}\n"
            "       # In TEMPLATES: set APP_DIRS=False and use an explicit `loaders` list that\n"
            "       # includes 'django_components.template_loader.Loader' (see the README).\n"
            "       # Add 'django_adminlte4.context_processors.adminlte' to context_processors.\n"
            "       DJANGO_VITE = {'default': {'dev_mode': DEBUG, "
            "'manifest_path': BASE_DIR / 'assets' / 'dist' / 'manifest.json'}}"
        )
        self.stdout.write("  4. Define your sidebar in settings.ADMINLTE = {'menu': [...]}")
        self.stdout.write(self.style.SUCCESS("\nAdminLTE 4 front-end installed."))
