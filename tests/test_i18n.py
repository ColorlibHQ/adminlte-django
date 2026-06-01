"""Polish: the package ships a translatable catalog (Spanish demo locale)."""

from django.utils import translation
from django.utils.translation import gettext, ngettext


def test_spanish_catalog_is_loaded():
    with translation.override("es"):
        assert gettext("Toggle sidebar") == "Alternar barra lateral"
        assert gettext("Log out") == "Cerrar sesión"
        assert gettext("View documentation") == "Ver documentación"


def test_spanish_plural_forms():
    with translation.override("es"):
        one = ngettext("Please correct the error below.", "Please correct the errors below.", 1)
        many = ngettext("Please correct the error below.", "Please correct the errors below.", 2)
        assert one == "Corrige el error a continuación."
        assert many == "Corrige los errores a continuación."


def test_english_falls_back_to_source():
    with translation.override("en"):
        assert gettext("Toggle sidebar") == "Toggle sidebar"
