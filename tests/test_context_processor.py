from django_adminlte4.context_processors import adminlte


def test_context_processor_exposes_config_and_menus(rf, settings):
    settings.ADMINLTE = {
        "title": "Ctx Test",
        "menu": [
            {"text": "Home", "url": "/"},
            {"text": "Top", "url": "t", "topnav": True},
        ],
    }
    ctx = adminlte(rf.get("/"))
    assert ctx["adminlte"]["title"] == "Ctx Test"
    assert "dark_mode" in ctx["adminlte"]
    assert len(ctx["adminlte_menu_sidebar"]) == 1
    assert len(ctx["adminlte_menu_navbar_left"]) == 1
    # Active state computed from the request path.
    assert ctx["adminlte_menu_sidebar"][0]["active"] is True


def test_dark_mode_flag(rf, settings):
    settings.ADMINLTE = {"layout_dark_mode": True, "menu": []}
    ctx = adminlte(rf.get("/"))
    assert ctx["adminlte"]["dark_mode"] is True
