# -*- coding: utf-8 -*-
"""Contains the activate command and helper methods.

Functions:
    activate: Activate the given project. If no project name is given, activate
        the current directory.
"""

import os
import pathlib

from .types import ProjectId


def activate(project: ProjectId = None):
    """
    Usage:
      containment activate [<project>]

    Arguments:
      <project>  The name of the project to activate.
    """
    _get_project_path(project)


def _get_project_path(project: ProjectId):
    """Find the path of the project based on the project name."""
    if not project:
        return pathlib.Path(os.getcwd())
    default_path = os.environ.get("CONTAINED_PROJECTS_PATH", ".")
    projects_path = pathlib.Path(default_path)
    matches = (p for p in projects_path.iterdir() if p == project)
    project_path = next(matches, None)
    if not project_path:
        raise ValueError('Unknown project "{}"'.format(project))
    return pathlib.Path(project_path)
