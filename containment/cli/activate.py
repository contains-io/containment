# -*- coding: utf-8 -*-
"""Contains the activate command and helper methods.

Functions:
    activate: Activate the given project. If no project name is given, activate
        the current directory.
"""
from ..builder import CommandLineInterface


def activate():
    """
    Usage:
      containment activate
    """
    # This is derived from the clone
    cli = CommandLineInterface()
    cli.ensure_config()
    cli.write_dockerfile()
    cli.build()
    cli.run()
