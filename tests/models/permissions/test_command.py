# -*- coding: utf-8 -*-

# django-mcadmin
# tests/models/permissions/test_user.py


from typing import List, Optional  # pylint: disable=W0611

from django.contrib.auth import get_user_model
from django.test import TestCase

from mcadmin.command import ManagementCommandAdmin
from mcadmin.models.command import Command
from mcadmin.models.permissions.command import CommandPermission
from mcadmin.template import ManagementCommandAdminTemplateFile


__all__ = ["CommandPermissionModelTest"]  # type: List[str]


User = get_user_model()


class TestManagementCommandAdminTemplateFile(ManagementCommandAdminTemplateFile):
    """
    Management command admin example file for tests.
    """

    path = "test.csv"
    description = "Test file"


class TestManagementCommandAdmin(ManagementCommandAdmin):
    """
    Management command admin for tests.
    """

    command = "test-command"
    name = "Test Command"
    templates = [TestManagementCommandAdminTemplateFile()]


class CommandPermissionModelTest(TestCase):
    """
    Command permission model tests.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """

        user = User.objects.create_user(
            username="test", password=User.objects.make_random_password()
        )
        command = Command.objects.create(
            command="tests.models.test_command.TestManagementCommandAdmin"
        )
        CommandPermission.objects.create(user=user, command=command)

    def test___unicode__(self):
        """
        __unicode__ method must return formatted group permission name.
        """

        command = CommandPermission.objects.first()  # type: Optional[CommandPermission]
        expected = "tests.models.test_command.TestManagementCommandAdmin - test"

        self.assertEqual(first=command.__unicode__(), second=expected)  # type: ignore

    def test___repr__(self):
        """
        __repr__ method must return formatted group permission name.
        """

        command = CommandPermission.objects.first()  # type: Optional[CommandPermission]
        expected = "tests.models.test_command.TestManagementCommandAdmin - test"

        self.assertEqual(
            first=command.__repr__(), second=expected,
        )

    def test___str__(self):
        """
        __str__ method must return formatted group permission name.
        """

        command = CommandPermission.objects.first()  # type: Optional[CommandPermission]
        expected = "tests.models.test_command.TestManagementCommandAdmin - test"

        self.assertEqual(
            first=command.__str__(), second=expected,
        )
