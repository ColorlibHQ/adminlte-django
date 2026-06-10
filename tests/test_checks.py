"""System checks (adminlte.W001 / E002 / W003 / W004)."""

from django.core import checks as django_checks

from django_adminlte4 import checks


def _ids(messages):
    return [m.id for m in messages]


def test_clean_settings_produce_no_messages(settings):
    settings.ADMINLTE = {"title": "OK", "menu": [{"text": "Home", "url": "/"}]}
    assert checks.check_unknown_settings() == []
    assert checks.check_menu_items() == []
    assert checks.check_template_engine() == []
    assert checks.check_context_processor() == []


def test_unknown_setting_warns(settings):
    settings.ADMINLTE = {"totally_unknown": 1}
    assert _ids(checks.check_unknown_settings()) == ["adminlte.W001"]


def test_menu_item_typo_warns(settings):
    settings.ADMINLTE = {
        "menu": [
            {"text": "Home", "url": "/", "lable": "NEW"},  # typo
            {"text": "Sub", "submenu": [{"txt": "oops"}]},  # typo + missing text
        ]
    }
    messages = checks.check_menu_items()
    assert all(m.id == "adminlte.W003" for m in messages)
    rendered = " ".join(str(m) for m in messages)
    assert "lable" in rendered and "txt" in rendered
    assert len(messages) == 3  # lable, txt, missing text/header/type


def test_missing_components_loader_is_error(settings):
    settings.TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,  # the classic misconfiguration
            "OPTIONS": {},
        }
    ]
    assert _ids(checks.check_template_engine()) == ["adminlte.E002"]
    assert _ids(checks.check_context_processor()) == ["adminlte.W004"]


def test_checks_are_registered():
    registered = {
        getattr(c, "__name__", "") for c in django_checks.registry.registry.registered_checks
    }
    assert {"check_unknown_settings", "check_template_engine", "check_menu_items"} <= registered
