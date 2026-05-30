import io

from django.core.management import call_command


def test_install_copies_stubs(tmp_path):
    out = io.StringIO()
    call_command("adminlte_install", "--path", str(tmp_path), stdout=out)
    assert (tmp_path / "assets" / "app.js").exists()
    assert (tmp_path / "assets" / "app.scss").exists()
    assert (tmp_path / "vite.config.js").exists()
    assert (tmp_path / "package.json").exists()
    assert "front-end installed" in out.getvalue()


def test_install_skips_existing_without_force(tmp_path):
    (tmp_path / "vite.config.js").write_text("// existing\n")
    out = io.StringIO()
    call_command("adminlte_install", "--path", str(tmp_path), stdout=out)
    assert "// existing" in (tmp_path / "vite.config.js").read_text()
    assert "exists" in out.getvalue()


def test_status_prints_version(tmp_path):
    out = io.StringIO()
    call_command("adminlte_status", stdout=out)
    text = out.getvalue()
    assert "django-adminlte4" in text
    assert "registered" in text


def test_scaffold_creates_crud_app(tmp_path):
    out = io.StringIO()
    call_command("adminlte_scaffold", "blog", "--path", str(tmp_path), stdout=out)
    assert (tmp_path / "blog" / "models.py").exists()
    assert (tmp_path / "blog" / "templates" / "blog" / "blog_list.html").exists()
    list_tpl = (tmp_path / "blog" / "templates" / "blog" / "blog_list.html").read_text()
    assert '{% component "adminlte_card"' in list_tpl
    assert "{{ obj.name }}" in list_tpl


def test_make_auth_creates_app(tmp_path):
    out = io.StringIO()
    call_command("adminlte_make_auth", "myauth", "--path", str(tmp_path), stdout=out)
    assert (tmp_path / "myauth" / "urls.py").exists()
    assert "LoginView" in (tmp_path / "myauth" / "urls.py").read_text()
