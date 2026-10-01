"""config/settings.py under production-like environments (fresh interpreter each).

The starter must refuse to run with DEBUG=False unless SECRET_KEY is a real key:
missing, empty or the published development key -> ImproperlyConfigured.
"""

import os
import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase

DEMO_DIR = Path(__file__).resolve().parent.parent
INSECURE = "django-insecure-dev-only-change-me"
REAL = "a-real-production-key-" + "x" * 40

PROBE = (
    "import django.conf, config.settings as s;"
    "print(s.SECRET_KEY == {real!r}, s.SECRET_KEY == {insecure!r}, "
    "s.STORAGES['staticfiles']['BACKEND'])"
)


def load_settings(**env):
    """Import config.settings in a subprocess with exactly these overrides."""
    environment = {
        k: v for k, v in os.environ.items()
        if k not in {"SECRET_KEY", "DEBUG", "DJANGO_SETTINGS_MODULE"}
    }
    environment.update(env)
    return subprocess.run(
        [sys.executable, "-c", PROBE.format(real=REAL, insecure=INSECURE)],
        cwd=DEMO_DIR, env=environment, capture_output=True, text=True, timeout=60, check=False,
    )


class SecretKeySettingsTests(SimpleTestCase):
    def assert_refuses(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("ImproperlyConfigured", result.stderr)
        self.assertIn("SECRET_KEY", result.stderr)

    def test_production_refuses_empty_key(self):
        self.assert_refuses(load_settings(DEBUG="False", SECRET_KEY=""))

    def test_production_refuses_blank_key(self):
        self.assert_refuses(load_settings(DEBUG="False", SECRET_KEY="   "))

    def test_production_refuses_the_published_dev_key(self):
        self.assert_refuses(load_settings(DEBUG="False", SECRET_KEY=INSECURE))

    def test_production_accepts_a_real_key(self):
        result = load_settings(DEBUG="False", SECRET_KEY=REAL)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.split(),
            ["True", "False", "django_adminlte4.storage.ViteCompressedManifestStaticFilesStorage"],
        )

    def test_debug_falls_back_to_the_dev_key(self):
        result = load_settings(DEBUG="True", SECRET_KEY="")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.split(),
            ["False", "True", "django.contrib.staticfiles.storage.StaticFilesStorage"],
        )
