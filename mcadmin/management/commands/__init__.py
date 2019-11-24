# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/management/commands/__init__.py


from typing import Any, Dict, List  # pylint: disable=W0611

from django.core.management.base import BaseCommand, CommandParser, no_translations
from django.utils.translation import ugettext_lazy as _


__all__ = ["TaskCommand"]  # type: List[str]


class TaskCommand(BaseCommand):
    """
    Management commands admin base task command class.
    Can run management command as background task.
    """

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Add command arguments.

        :param parser: command arguments parser instance.
        :type parser: django.core.management.base.CommandParser.
        :return: nothing.
        :rtype: None.
        """

        parser.add_argument(
            "--task",
            "-T",
            dest="as_task",
            help=_("Run command as background task"),
            default=False,
            action="store_true",
            metavar="TASK",
            type=bool,
        )

    @no_translations
    def handle(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Detect how to run command.

        :param args: additional args.
        :type args: List[Any].
        :param kwargs: additional args.
        :type kwargs: Dict[str, Any].
        :return: nothing.
        :rtype: None.
        """

        if kwargs.get("as_task", False):
            self._as_task(*args, **kwargs)
        else:
            self._local(*args, **kwargs)

    def _local(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Must be implemented in child class.
        Run command locally.

        :param args: additional args.
        :type args: List[Any].
        :param kwargs: additional args.
        :type kwargs: Dict[str, Any].
        :return: nothing.
        :rtype: None.
        """

        raise NotImplementedError

    def _as_task(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """
        Must be implemented in child class.
        Run command as background task.

        :param args: additional args.
        :type args: List[Any].
        :param kwargs: additional args.
        :type kwargs: Dict[str, Any].
        :return: nothing.
        :rtype: None.
        """

        raise NotImplementedError
