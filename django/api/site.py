from django.contrib.admin import AdminSite


class ITVRAdminSite(AdminSite):
    def refine_app(self, app):
        models = app.get("models")
        if models is not None:
            for model in models:
                model_cls = model["model"]
                if hasattr(model_cls, "admin_label"):
                    model["admin_label"] = model_cls.admin_label
                else:
                    model["admin_label"] = model["name"]
                if hasattr(model_cls, "admin_hide_view_change_buttons"):
                    model["admin_hide_view_change_buttons"] = (
                        model_cls.admin_hide_view_change_buttons
                    )
                else:
                    model["admin_hide_view_change_buttons"] = False

    def _build_app_dict(self, request, label=None):
        app_dict = super()._build_app_dict(request, label)
        if label:
            self.refine_app(app_dict)
        else:
            for app in app_dict.values():
                self.refine_app(app)
        return app_dict
