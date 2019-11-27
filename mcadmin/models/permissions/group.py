# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/models/permissions/group.py


from typing import List  # pylint: disable=W0611

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


__all__ = ["GroupPermission"]  # type: List[str]


class GroupPermission(models.Model):
    """
    Management commands admin commands group permissions.
    """

    group = models.ForeignKey(
        "mcadmin.Group",
        verbose_name=_("group"),
        db_index=True,
        related_name="permissions",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        db_index=True,
        on_delete=models.CASCADE,
        related_name="mcadmin_groups",
    )

    def __unicode__(self) -> str:

        return f"{self.group} - {self.user}"

    def __str__(self) -> str:

        return self.__unicode__()

    def __repr__(self) -> str:

        return self.__unicode__()

    class Meta:

        app_label = "mcadmin"  # type: str
        unique_together = [
            "group",
            "user",
        ]  # type: List[str]
        verbose_name = _("management command group permission")  # type: str
        verbose_name_plural = _("management command group permissions")  # type: str
        ordering = [
            "group",
        ]  # type: List[str]
