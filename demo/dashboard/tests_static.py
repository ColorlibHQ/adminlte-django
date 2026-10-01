"""Production static pipeline on the real Vite build (needs `npm run build`).

0.3.0 bug: WhiteNoise re-hashed Vite's output, the page loaded the entry as
``app-XXXX.<hash>.js`` and the lazily imported Quill chunk imported
``./app-XXXX.js`` — a second copy of the app, so the sidebar toggle (and every
other handler) fired twice on the Components page. Collect the real build with
the production storage and check that every relative module import in the
collected JavaScript resolves to the URL the page loads for that module.
"""

import json
import posixpath
import re
import tempfile
import unittest
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import SimpleTestCase, override_settings

DIST = Path(settings.BASE_DIR) / "assets" / "dist"
PRODUCTION_STORAGE = "django_adminlte4.storage.ViteCompressedManifestStaticFilesStorage"
JS_IMPORT = re.compile(r"""(?:\bfrom\s*|\bimport\s*\(?\s*)(["'`])(\.{1,2}/[^"'`]+?\.m?js)\1""")


@unittest.skipUnless((DIST / "manifest.json").exists(), "run `npm run build` first")
class ProductionStaticFilesTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls._tmp.name)
        with override_settings(
            STATIC_ROOT=cls.root,
            STORAGES={**settings.STORAGES, "staticfiles": {"BACKEND": PRODUCTION_STORAGE}},
        ):
            call_command("collectstatic", interactive=False, clear=True, verbosity=0)
        cls.paths = json.loads((cls.root / "staticfiles.json").read_text())["paths"]
        cls.vite = json.loads((DIST / "manifest.json").read_text())

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()
        super().tearDownClass()

    def test_vite_files_are_not_rehashed(self):
        for chunk in self.vite.values():
            for name in [chunk["file"], *chunk.get("css", []), *chunk.get("assets", [])]:
                self.assertEqual(self.paths[name], name)

    def test_every_relative_import_resolves_to_the_url_the_page_loads(self):
        checked, problems = 0, []
        for original, stored in self.paths.items():
            if not stored.endswith(".js"):
                continue
            source = (self.root / stored).read_text(encoding="utf-8")
            for _q, spec in JS_IMPORT.findall(source):
                fetched = posixpath.normpath(posixpath.join(posixpath.dirname(stored), spec))
                target = posixpath.normpath(posixpath.join(posixpath.dirname(original), spec))
                expected = self.paths.get(target)
                checked += 1
                if expected is None:
                    problems.append(f"{original}: {spec} not collected")
                elif fetched != expected:
                    problems.append(f"{original}: {spec} -> {fetched}, page loads {expected}")
        self.assertGreater(checked, 10)  # the chunk graph really was inspected
        self.assertEqual(problems, [])

    def test_lazy_chunks_that_import_the_entry_get_the_same_module(self):
        entry = next(c["file"] for c in self.vite.values() if c.get("isEntry"))
        importers = [
            c["file"] for c in self.vite.values()
            if c["file"].endswith(".js")
            and f'"./{posixpath.basename(entry)}"' in (self.root / self.paths[c["file"]]).read_text()
        ]
        for name in importers:  # e.g. the Quill chunk, which imports shared code from the entry
            self.assertEqual(self.paths[entry], entry, name)
