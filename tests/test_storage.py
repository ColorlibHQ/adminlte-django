"""Vite-aware manifest storages (django_adminlte4.storage).

Regression for 0.3.0's "sidebar toggle fires twice": with Django's/WhiteNoise's
manifest storage the page loaded the Vite entry under a second, Django-hashed
name while lazily imported chunks imported it by its Vite name, so the browser
ran two copies of the app. The invariant checked here — and on the real demo
build in ``demo/dashboard/tests_static.py`` — is that every relative module
import inside the collected JavaScript resolves to exactly the URL that
``static()`` (what ``{% vite_asset %}`` emits) gives the page for that file.
"""

from __future__ import annotations

import json
import posixpath
import re
from pathlib import Path

import pytest
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.management import call_command
from django.templatetags.static import static
from django.test import override_settings

from django_adminlte4.storage import (
    ViteManifestStaticFilesStorage,
    immutable_file_test,
    vite_manifest_files,
)

# Static `import … from "./x.js"`, side-effect `import "./x.js"`, re-exports, and
# dynamic import("./x.js") / import(`./x.js`) — the forms Vite/rolldown emit.
JS_IMPORT = re.compile(
    r"""(?:\bfrom\s*|\bimport\s*\(?\s*)(["'`])(\.{1,2}/[^"'`]+?\.m?js)\1"""
)

WHITENOISE = "django_adminlte4.storage.ViteCompressedManifestStaticFilesStorage"
DJANGO = "django_adminlte4.storage.ViteManifestStaticFilesStorage"


def relative_import_mismatches(static_root: Path, static_url: str = "/static/") -> list[str]:
    """Relative imports in collected JS whose URL differs from static(target)."""
    paths = json.loads((static_root / "staticfiles.json").read_text())["paths"]
    stored = set(paths.values())
    problems = []
    for original, stored_name in paths.items():
        if not stored_name.endswith(".js"):
            continue
        source = (static_root / stored_name).read_text(encoding="utf-8")
        for _quote, spec in JS_IMPORT.findall(source):
            # What the browser fetches: resolved against the importing file's URL.
            fetched = posixpath.normpath(posixpath.join(posixpath.dirname(stored_name), spec))
            # What the page loads for that module (django-vite -> static()).
            target = posixpath.normpath(posixpath.join(posixpath.dirname(original), spec))
            expected = paths.get(target)
            if expected is None:
                if fetched not in stored:
                    problems.append(f"{original}: {spec} -> {fetched} (not collected)")
                continue
            if fetched != expected:
                problems.append(f"{original}: {spec} -> {fetched}, page loads {expected}")
    return problems


def _vite_build(root: Path) -> Path:
    """A miniature Vite build: entry + lazy chunk that imports the entry back."""
    dist = root / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "assets" / "app-AbC12_-9.js").write_text(
        'export const n=1;const l={quill:()=>import(`./quill-QwErTy12.js`)};'
        'import"./vendor-ZxCvB678.js";window.adminlteUse=l;\n'
    )
    (dist / "assets" / "quill-QwErTy12.js").write_text(
        'import{n as e}from"./app-AbC12_-9.js";export default e;\n'
    )
    (dist / "assets" / "vendor-ZxCvB678.js").write_text("export const v=2;\n")
    (dist / "assets" / "app-CsS00000.css").write_text(
        '@font-face{src:url("/static/assets/icons-FoNt0000.woff2?abc#iefix")}\n'
        '.x{background:url("../plain.png")}\n'
    )
    (dist / "assets" / "icons-FoNt0000.woff2").write_bytes(b"\x00font")
    (dist / "plain.png").write_bytes(b"\x89PNGdata")  # not listed in the manifest
    (dist / "manifest.json").write_text(json.dumps({
        "assets/app.js": {
            "file": "assets/app-AbC12_-9.js",
            "isEntry": True,
            "imports": ["_vendor.js"],
            "dynamicImports": ["node_modules/quill/quill.js"],
            "css": ["assets/app-CsS00000.css"],
            "assets": ["assets/icons-FoNt0000.woff2"],
        },
        "_vendor.js": {"file": "assets/vendor-ZxCvB678.js"},
        "node_modules/quill/quill.js": {"file": "assets/quill-QwErTy12.js", "isDynamicEntry": True},
    }))
    return dist


@pytest.fixture
def collect(tmp_path):
    def run(backend: str) -> Path:
        dist = _vite_build(tmp_path / "src")
        root = tmp_path / "out"
        with override_settings(
            STATIC_ROOT=root,
            STATICFILES_DIRS=[dist],
            STATICFILES_FINDERS=["django.contrib.staticfiles.finders.FileSystemFinder"],
            STORAGES={
                "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
                "staticfiles": {"BACKEND": backend},
            },
        ):
            call_command("collectstatic", interactive=False, clear=True, verbosity=0)
        return root

    return run


@pytest.mark.parametrize("backend", [DJANGO, WHITENOISE])
def test_vite_files_keep_their_names(collect, backend):
    if backend == WHITENOISE:
        pytest.importorskip("whitenoise")
    root = collect(backend)
    paths = json.loads((root / "staticfiles.json").read_text())["paths"]
    for name in [
        "assets/app-AbC12_-9.js",
        "assets/quill-QwErTy12.js",
        "assets/vendor-ZxCvB678.js",
        "assets/app-CsS00000.css",
        "assets/icons-FoNt0000.woff2",
    ]:
        assert paths[name] == name
    # files the Vite manifest does not list are hashed as usual
    assert re.fullmatch(r"plain\.[0-9a-f]{12}\.png", paths["plain.png"])
    assert re.fullmatch(r"manifest\.[0-9a-f]{12}\.json", paths["manifest.json"])
    # CSS references keep query + fragment and point at existing files
    css = (root / "assets" / "app-CsS00000.css").read_text()
    assert 'url("/static/assets/icons-FoNt0000.woff2?abc#iefix")' in css
    assert re.search(r'url\("\.\./plain\.[0-9a-f]{12}\.png"\)', css)
    assert relative_import_mismatches(root) == []


@pytest.mark.parametrize("backend", [DJANGO, WHITENOISE])
def test_page_and_chunks_load_one_url_per_module(collect, backend, settings):
    if backend == WHITENOISE:
        pytest.importorskip("whitenoise")
    root = collect(backend)
    settings.STATIC_ROOT = root
    settings.STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": backend},
    }
    settings.DEBUG = False
    staticfiles_storage._setup()
    # what {% vite_asset %} renders for the entry == what the chunk imports
    assert static("assets/app-AbC12_-9.js") == "/static/assets/app-AbC12_-9.js"


def test_plain_manifest_storage_reproduces_the_double_load(collect):
    """Control: the checker catches 0.3.0's bug with the stock storage."""
    root = collect("django.contrib.staticfiles.storage.ManifestStaticFilesStorage")
    problems = relative_import_mismatches(root)
    assert any("quill" in p and "app-AbC12_-9" in p for p in problems), problems


def test_vite_manifest_files_handles_dot_vite_dir_and_rejects_other_json():
    data = {"a.js": {"file": "assets/a-12345678.js", "css": ["assets/a-87654321.css"]}}
    assert vite_manifest_files("build/.vite/manifest.json", data) == {
        "build/assets/a-12345678.js",
        "build/assets/a-87654321.css",
    }
    assert vite_manifest_files("manifest.json", {"name": "app", "icons": []}) == set()
    assert vite_manifest_files("manifest.json", []) == set()


def test_unrelated_manifest_json_is_ignored(tmp_path):
    """A PWA-style manifest.json must not stop files from being hashed."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"name": "x", "start_url": "/"}))
    (src / "app.js").write_text("console.log(1)\n")
    with override_settings(
        STATIC_ROOT=tmp_path / "out",
        STATICFILES_DIRS=[src],
        STATICFILES_FINDERS=["django.contrib.staticfiles.finders.FileSystemFinder"],
        STORAGES={
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {"BACKEND": DJANGO},
        },
    ):
        call_command("collectstatic", interactive=False, clear=True, verbosity=0)
    paths = json.loads((tmp_path / "out" / "staticfiles.json").read_text())["paths"]
    assert re.fullmatch(r"app\.[0-9a-f]{12}\.js", paths["app.js"])


def test_immutable_file_test(settings, monkeypatch):
    settings.STATIC_URL = "/static/"
    storage = ViteManifestStaticFilesStorage(location="/nonexistent")
    storage.hashed_files = {
        "assets/app-AbC12_-9.js": "assets/app-AbC12_-9.js",
        "css/site.css": "css/site.0123456789ab.css",
        "img/icon-settings.svg": "img/icon-settings.0123456789ab.svg",
    }
    monkeypatch.setattr(staticfiles_storage, "_wrapped", storage)
    assert immutable_file_test("", "/static/assets/app-AbC12_-9.js")         # Vite-hashed
    assert immutable_file_test("", "/static/css/site.0123456789ab.css")     # Django-hashed
    assert not immutable_file_test("", "/static/css/site.css")              # original name
    assert not immutable_file_test("", "/static/img/icon-settings.svg")     # looks hashed, isn't
    assert not immutable_file_test("", "/media/a-AbC12_-9.js")              # not static
