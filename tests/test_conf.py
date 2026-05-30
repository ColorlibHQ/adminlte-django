import warnings

from django_adminlte4.conf import DEFAULTS, get_config, validate_config


def test_defaults_present():
    cfg = get_config()
    assert cfg["title"]
    assert cfg["sidebar_theme"] == "dark"
    assert isinstance(cfg["menu"], list)
    assert len(cfg["filters"]) == 4


def test_user_overrides(settings):
    settings.ADMINLTE = {"title": "Custom", "sidebar_theme": "light"}
    cfg = get_config()
    assert cfg["title"] == "Custom"
    assert cfg["sidebar_theme"] == "light"
    # An untouched key still falls back to the default.
    assert cfg["sidebar_mini"] == DEFAULTS["sidebar_mini"]


def test_unknown_key_warns(settings):
    settings.ADMINLTE = {"totally_unknown": 1}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        unknown = validate_config()
    assert "totally_unknown" in unknown
    assert any("Unknown ADMINLTE setting" in str(w.message) for w in caught)
