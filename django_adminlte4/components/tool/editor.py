import json

from django_components import Component, register

from django_adminlte4.component_utils import field_state, render_attrs


@register("adminlte_editor")
class Editor(Component):
    """Quill rich-text editor. Port of ``Tool\\Editor``.

    Emits a hidden input (the form value) plus a ``data-quill`` container that
    the plugin initializer mounts Quill onto, syncing HTML back to the input.
    Bind a Django field via ``field=form.body`` or use ``name``/``value``.
    """

    template_file = "editor.html"

    def get_template_data(self, args, kwargs, slots, context):
        kwargs = dict(kwargs)
        fgroup_class = kwargs.pop("fgroup_class", "")
        placeholder = kwargs.pop("placeholder", "Enter text...")
        quill_options = kwargs.pop("quill_options", None) or {}
        editor_id = kwargs.get("id")  # field_state pops 'id'
        state = field_state(kwargs)
        if not editor_id:
            editor_id = state["id"]
        config = {"theme": "snow", "placeholder": placeholder}
        config.update(quill_options)
        return {
            **state,
            "editor_id": editor_id,
            "fgroup_class": fgroup_class,
            "config_json": json.dumps(config),
            "attrs": render_attrs(kwargs),
        }
