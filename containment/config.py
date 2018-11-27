# -*- coding: utf-8 -*-
"""Contains the configuration for the containment."""
import grp
import os
from pathlib import Path
from typing import List

from typet import Bounded
from typet import Object
from typet import singleton

from .exceptions import DockerGroupMissing
from .types.environment import EnvironmentVariable


_PROJECT_ROOT = Path(os.getcwd())
_HOME = Path(os.path.expanduser("~"))
_SHELL = Path(EnvironmentVariable("SHELL").value)


def _get_docker_gid() -> Bounded[int, 0]:
    try:
        return grp.getgrnam("docker").gr_gid
    except KeyError:
        raise DockerGroupMissing


@singleton
class _ProjectConfig(Object):
    path: Path = _PROJECT_ROOT / ".containment"
    base: Path = path / "base"
    os_packages: Path = path / "os_packages.json"
    lang_packages: Path = path / "lang_packages.json"


@singleton
class _PersonalConfig(Object):
    path: Path = _HOME / ".containment"
    projects: Path = path / "projects"
    os_packages: Path = path / "os_packages.json"
    lang_packages: Path = path / "lang_packages.json"
    package_list: List[str] = ["docker", _SHELL.name]


@singleton
class _ProjectCustomization(Object):
    path: Path = _HOME / ".containment" / "projects" / _PROJECT_ROOT.name
    dockerfile: Path = path / "Dockerfile"
    runfile: Path = path / "run_containment.sh"
    entrypoint: Path = path / "entrypoint.sh"
    os_packages: Path = path / "os_packages.json"
    lang_packages: Path = path / "lang_packages.json"


@singleton
class _Config(Object):
    name: Path = _PROJECT_ROOT.name
    tag: str = f"containment/{name}"
    uid: int = os.getuid()
    user: str = os.path.basename(os.path.expanduser("~"))
    docker_gid: int = _get_docker_gid()
    shell: Path = _SHELL
    home: Path = _HOME
    project_config: _ProjectConfig = _ProjectConfig()
    personal_config: _PersonalConfig = _PersonalConfig()
    project_customization: _ProjectCustomization = _ProjectCustomization()


settings = _Config()
