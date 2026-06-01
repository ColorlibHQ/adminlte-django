# Configuration

All behaviour is configured through a single `ADMINLTE` dict in your settings,
shallow-merged over the defaults in `django_adminlte4.conf.DEFAULTS`. Unknown
top-level keys emit a warning at startup. Every key below is optional.

```python
ADMINLTE = {
    "title": "My Dashboard",
    "logo": "<b>My</b>App",
    "sidebar_theme": "light",
}
```

## Title

| Key | Default | Description |
|---|---|---|
| `title` | `"AdminLTE 4"` | Base page/site title. |
| `title_prefix` | `""` | Prepended to every page title. |
| `title_postfix` | `""` | Appended to every page title. |

## Logo & brand

| Key | Default | Description |
|---|---|---|
| `logo` | `"<b>Admin</b>LTE"` | Brand lockup (HTML allowed) — sidebar brand & auth header. |
| `logo_alt_text` | `"AdminLTE 4"` | Sidebar brand text next to the logo image. |
| `logo_img` | `"adminlte/img/AdminLTELogo.png"` | Brand image static path. |
| `logo_img_class` | `"brand-image opacity-75 shadow"` | Classes on the brand image. |
| `logo_img_alt` | `"AdminLTE Logo"` | Brand image `alt`. |

## Topbar (navbar)

| Key | Default | Description |
|---|---|---|
| `navbar_search` | `True` | Show the navbar search trigger. |
| `navbar_messages` | `None` | Messages dropdown data: `{"count": int, "items": [...]}` (omit to hide). |
| `navbar_notifications` | `None` | Notifications dropdown data (same shape). |

See [Sidebar menu → Topbar dropdowns](menu.md#topbar-dropdowns) for the item shape.

## User menu

| Key | Default | Description |
|---|---|---|
| `usermenu` | `None` | Rich user card: `{"image","name","description","since","stats"}`. Shown only to **authenticated** users; logged-out visitors get the simple Guest menu with a Sign in link. Omit to fall back to the Django-user menu for everyone. |
| `usermenu_enabled` | `True` | Show the user menu at all. |
| `usermenu_header` | `False` | Show the colored header in the simple menu. |
| `usermenu_header_class` | `"bg-primary"` | Header background class. |
| `usermenu_image` | `False` | Show the user avatar. |
| `usermenu_desc` | `False` | Show the user description line. |
| `usermenu_profile_url` | `False` | Profile link target. |
| `auth_logo_enabled` | `False` | Show the logo on auth pages. |

## Layout

| Key | Default | Description |
|---|---|---|
| `layout_topnav` | `None` | Top-navigation (no sidebar) layout. |
| `layout_boxed` | `None` | Boxed layout. |
| `layout_fixed_sidebar` | `True` | `.layout-fixed` — fixed, scrollable sidebar. |
| `layout_fixed_navbar` | `True` | `.fixed-header` — sticky topbar. |
| `layout_fixed_footer` | `None` | `.fixed-footer`. |
| `layout_dark_mode` | `None` | Force dark mode (`None` = respect system / the toggle). |
| `layout_rtl` | `False` | Right-to-left layout (loads the RTL stylesheet). |

## Footer, preloader & control sidebar

| Key | Default | Description |
|---|---|---|
| `footer_left` | Copyright string | Footer left content (HTML allowed). |
| `footer_right` | `"Anything you want"` | Footer right content. |
| `preloader` | `False` | Show the page preloader. |
| `control_sidebar` | `False` | Enable the right control sidebar. |
| `control_sidebar_theme` | `"dark"` | Control-sidebar theme. |
| `sidebar_docs_url` | `https://django.adminlte.io/docs/` | Docs link used by the sidebar "View documentation" CTA **and** the topbar Documentation link. |

## Sidebar

| Key | Default | Description |
|---|---|---|
| `sidebar_breakpoint` | `"lg"` | `sidebar-expand-{breakpoint}`. |
| `sidebar_mini` | `True` | `.sidebar-mini` — collapse to an icon rail. |
| `sidebar_collapse` | `False` | Start collapsed. |
| `sidebar_theme` | `"dark"` | `"dark"` or `"light"` sidebar. |

## Custom CSS classes

Append your own classes to layout elements:

| Key | Default |
|---|---|
| `classes_body` | `""` |
| `classes_brand` | `""` |
| `classes_brand_text` | `"fw-light"` |
| `classes_content_header` | `""` |
| `classes_content` | `""` |
| `classes_sidebar` | `"bg-body-secondary shadow"` |
| `classes_sidebar_nav` | `""` |
| `classes_topnav` | `"navbar-expand bg-body"` |
| `classes_topnav_container` | `"container-fluid"` |

## Color mode

| Key | Default | Description |
|---|---|---|
| `color_mode_toggle` | `True` | Show the Light / Dark / Auto switcher in the topbar. |

## Assets

| Key | Default | Description |
|---|---|---|
| `assets_mode` | `"vite"` | `"vite"` (django-vite/HMR) or `"static"` (shipped bundle, no Node). See [Assets](assets.md). |

## Django admin

| Key | Default | Description |
|---|---|---|
| `admin_enabled` | `True` | Apply the AdminLTE skin to `django.contrib.admin`. |
| `admin_brand` | `""` | Admin sidebar brand text (falls back to `site_header`). |
| `admin_menu` | `None` | Override the auto app/model sidebar with explicit menu-item dicts. |

See [Django admin](admin.md).

## Menu & pipeline

| Key | Default | Description |
|---|---|---|
| `menu` | `[]` | The sidebar/topnav menu definition. See [Sidebar menu](menu.md). |
| `filters` | `GateFilter, HrefFilter, ActiveFilter, SearchFilter` | Ordered dotted-path filter pipeline applied per request. |
| `plugins` | `{}` | Reserved for plugin configuration. |
