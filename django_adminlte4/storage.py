"""Static-files storages that leave Vite's build output alone.

Vite already content-hashes every file it emits (``assets/app-CjSNY8Oz.js``)
and its chunks import each other by those names (``import … from
"./app-CjSNY8Oz.js"``). Django's ``ManifestStaticFilesStorage`` — and
WhiteNoise's ``CompressedManifestStaticFilesStorage`` on top of it — hash them a
*second* time (``app-CjSNY8Oz.4f2a…e1.js``) and the page loads that name via
``{% vite_asset %}``/``static()``, but it does not rewrite the imports inside
the JavaScript. A lazily loaded chunk that imports the entry (or a chunk the
page loaded) then fetches it under its Vite name: a different URL, so the
browser evaluates a **second copy** of the app — every event listener is bound
twice, and e.g. the AdminLTE sidebar toggle opens and closes on one click.

These storages detect Vite manifests among the collected files
(``manifest.json`` / ``.vite/manifest.json``) and store every file a manifest
lists under its own (already hashed) name, so the page and the chunks agree on
one URL per module. Everything else is hashed exactly as before.

Use them in production settings::

    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            # with WhiteNoise:
            "BACKEND": "django_adminlte4.storage.ViteCompressedManifestStaticFilesStorage",
            # or without it:
            # "BACKEND": "django_adminlte4.storage.ViteManifestStaticFilesStorage",
        },
    }

With WhiteNoise serving the files, also set ``WHITENOISE_IMMUTABLE_FILE_TEST``
to :func:`immutable_file_test` so Vite's hashed files get far-future cache
headers like Django-hashed ones.
"""

from __future__ import annotations

import json
import posixpath
import re
from typing import Any
from urllib.parse import urlsplit

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

#: Basenames that may hold a Vite build manifest (``build.manifest`` = true
#: writes ``.vite/manifest.json``; projects often set ``"manifest.json"``).
VITE_MANIFEST_NAMES = frozenset({"manifest.json"})


def vite_manifest_files(manifest_name: str, data: Any) -> set[str]:
    """Static names of the files a parsed Vite manifest lists.

    ``manifest_name`` is the manifest's own static path; Vite's paths are
    relative to the build ``outDir``, which is the manifest's directory (or
    its parent, for ``.vite/manifest.json``). Returns an empty set when
    ``data`` is not a Vite manifest.
    """
    if not isinstance(data, dict) or not data:
        return set()
    if not all(isinstance(chunk, dict) and isinstance(chunk.get("file"), str) for chunk in data.values()):
        return set()
    base = posixpath.dirname(manifest_name)
    if posixpath.basename(base) == ".vite":
        base = posixpath.dirname(base)
    files: set[str] = set()
    for chunk in data.values():
        for path in [chunk["file"], *chunk.get("css", []), *chunk.get("assets", [])]:
            if isinstance(path, str):
                files.add(posixpath.normpath(posixpath.join(base, path)))
    return files


class ViteManifestFilesMixin:
    """Keep Vite-built files under their own names in a manifest storage.

    Mix in *before* a ``ManifestFilesMixin`` storage. Vite manifests are found
    among the files ``collectstatic`` passes to ``post_process``; every file
    they list keeps its name (it is recorded in ``staticfiles.json`` mapping
    to itself, so ``static()`` returns it unchanged), while CSS files are still
    scanned so their ``url()`` references resolve.
    """

    _vite_files: frozenset[str] = frozenset()

    def post_process(self, paths: dict[str, Any], dry_run: bool = False, **options: Any):
        files: set[str] = set()
        for name, (storage, path) in paths.items():
            clean = name.replace("\\", "/")
            if posixpath.basename(clean) not in VITE_MANIFEST_NAMES:
                continue
            try:
                with storage.open(path) as handle:
                    data = json.loads(handle.read().decode("utf-8"))
            except (OSError, ValueError):
                continue
            files |= vite_manifest_files(clean, data)
        self._vite_files = frozenset(files)
        try:
            yield from super().post_process(paths, dry_run=dry_run, **options)  # type: ignore[misc]
        finally:
            self._vite_files = frozenset()

    def is_vite_file(self, name: str) -> bool:
        # CSS references reach hashed_name() with their query/fragment
        # (``fonts/x-AbC123.woff2?v=1#iefix``); match on the path alone.
        path = urlsplit(name.replace("\\", "/")).path
        return bool(path) and posixpath.normpath(path) in self._vite_files

    def hashed_name(self, name: str, content: Any = None, filename: str | None = None) -> str:
        if self.is_vite_file(name):
            return name  # keeps any ?query/#fragment, like Django's hashed_name()
        return super().hashed_name(name, content, filename)  # type: ignore[misc]


class ViteManifestStaticFilesStorage(ViteManifestFilesMixin, ManifestStaticFilesStorage):
    """``ManifestStaticFilesStorage`` that does not re-hash Vite output."""


try:
    from whitenoise.storage import CompressedManifestStaticFilesStorage
except ImportError:  # WhiteNoise is optional
    pass
else:

    class ViteCompressedManifestStaticFilesStorage(
        ViteManifestFilesMixin, CompressedManifestStaticFilesStorage
    ):
        """WhiteNoise's compressed manifest storage that does not re-hash Vite output."""


_DJANGO_HASH = re.compile(r"\.[0-9a-f]{12}\.[^./]+$")
_VITE_HASH = re.compile(r"-[A-Za-z0-9_-]{8}\.[^./]+$")


def immutable_file_test(path: str, url: str) -> bool:
    """``WHITENOISE_IMMUTABLE_FILE_TEST`` that also recognises Vite's hashes.

    WhiteNoise's default only recognises Django's 12-hex-digit hashes, so
    files kept under their Vite names would get a short ``max-age``. A Vite
    file counts as immutable when the static manifest maps it to itself (only
    files a Vite manifest listed are stored that way) and its name carries a
    Vite content hash. Assign the function itself, not its dotted path
    (WhiteNoise treats a string as a regex)::

        from django_adminlte4.storage import immutable_file_test
        WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test
    """
    from django.conf import settings
    from django.contrib.staticfiles.storage import staticfiles_storage

    prefix = urlsplit(settings.STATIC_URL or "/").path
    if not url.startswith(prefix):
        return False
    name = url[len(prefix):]
    if _DJANGO_HASH.search(name):
        return True
    hashed_files = getattr(staticfiles_storage, "hashed_files", None) or {}
    return hashed_files.get(name) == name and bool(_VITE_HASH.search(name))
