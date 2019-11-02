# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/views.py

from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from mcadmin.forms import ManagementCommandAdminFormWithFiles
from mcadmin.utils import CommandsLoader


__all__ = [
    "Index",
]


class Index(TemplateView):
    """
    Main management commands admin view.
    """

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        """
        Overload dispatch to add staff user required checking.
        """

        return super(Index, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Populate context.
        """

        context = super(Index, self).get_context_data(**kwargs)
        context["title"] = _("Management commands")  # need to show in page title
        context["loader"] = self.loader(self.request)

        return context

    def post(self, request, *args, **kwargs):
        """
        POST request processing.
        """

        command = self.loader(request).commands[
            list(set(self.loader(request).commands.keys()) & set(request.POST.keys()))[
                0
            ]
        ]  # get first command from POST data
        command.form = command.form(request.POST, request.FILES)

        if command.form.is_valid():
            if (
                isinstance(command.form, ManagementCommandAdminFormWithFiles)
                and command.templates
            ):  # check if form have files
                command.form.save_files()
            try:
                command.handle(
                    *command.form2args(request.POST),
                    **command.form2kwargs(request.POST)
                )
                messages.success(
                    request,
                    _("Run '{command}' management command success").format(
                        command=command.name
                    ),
                )
            except Exception as err:
                messages.error(
                    request,
                    _("Running '{command}' management command error: {err}").format(
                        command=command.name, err=err
                    ),
                )
        else:
            messages.error(
                request,
                _("This form was completed with errors: {command}").format(
                    command=command.name
                ),
            )

        return self.render_to_response(self.get_context_data(**kwargs))

    def loader(self, request):
        """
        Cache loader.
        """

        return CommandsLoader(request=request)

    def get_template_names(self):
        """
        Get template.
        """

        return [
            "mcadmin/index.html",
        ]
