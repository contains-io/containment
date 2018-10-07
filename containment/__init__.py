# -*- coding: utf-8 -*-
"""Contains the top-level contain command and helper methods.

Functions:
    contain: Run the given subcommand. If no subcommand is given, activate the
        current directory.
"""

from . import activate, init


def containment():
    """
    Usage:
      containment [--log-level <level> | --debug | --verbose] [<project>]
      containment [--log-level <level> | --debug | --verbose]
              [<command> [<args>...]]
      containment (-h | --help)
      containment (-V | --version)

    Options:
      -h, --help           Display this help message and exit.
      -V, --version        Display the version and exit.
      -d, --debug          Set the log level to DEBUG.
      -v, --verbose        Set the log level to INFO.
      --log-level <level>  Set the log level to one of DEBUG, INFO, WARN, or
                           ERROR.

    '{command} help -a' lists all available subcommands.
    See '{command} help <command>' for more information on a specific command.
    """
    init.init()
    activate.activate()
