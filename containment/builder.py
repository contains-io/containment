# -*- coding: utf-8 -*-
import json
import os
import pathlib
import subprocess
import sys

import docker

from .config import settings


class Context:
    def __init__(self):
        settings.docker_gid = subprocess.getoutput(
            "grep docker /etc/group"
        ).split(":")[2]
        # CONFIGURATION STRINGS
        self.project_adapter = f"""RUN     useradd -G docker --uid {settings.uid} --home /home/{settings.user} {settings.user}
        RUN     echo {settings.user} ALL=\(ALL\) NOPASSWD: ALL >> /etc/sudoers
        COPY    ./entrypoint.sh entrypoint.sh
        RUN     chmod +x entrypoint.sh"""
        self.entrypoint_text = f"""#!{settings.shell}
        cd {settings.project_config.path}
        sudo sed -ie 's/docker:x:[0-9]*:{settings.user}/docker:x:{settings.docker_gid}:{settings.user}/g' /etc/group
        sudo usermod -s {settings.shell} {settings.user}
        exec {settings.shell}"""
        try:
            ssh_auth_sock = os.environ["SSH_AUTH_SOCK"]
        except KeyError:
            ssh_auth_sock = ""
        if ssh_auth_sock:
            ssh_auth_sock_parent = pathlib.Path(
                ssh_auth_sock
            ).parent.as_posix()
            self.run_text = f"""docker run -it \
                           -v /var/run/docker.sock:/var/run/docker.sock \
                           -v {settings.home}:{settings.home} \
                           -v {settings.project_config.path}:{settings.project_config.path} \
                           -v {ssh_auth_sock_parent} \
                           -e SSH_AUTH_SOCK={ssh_auth_sock} \
                           --entrypoint=/entrypoint.sh -u {settings.user}:{settings.docker_gid} {settings.tag}:latest"""
        else:
            self.run_text = f"""docker run -it \
                           -v /var/run/docker.sock:/var/run/docker.sock \
                           -v {settings.home}:{settings.home} \
                           -v {settings.project_config.path}:{settings.project_config.path} \
                           --entrypoint=/entrypoint.sh -u {settings.user}:{settings.docker_gid} {settings.tag}:latest"""

        self.externalbasis = "ubuntu"
        self.base_text = f"""FROM    {self.externalbasis}
        RUN     apt update && apt install -y sudo docker.io"""


class CommandLineInterface:
    def __init__(self):
        self.context = Context()
        self.pkg_install_cmds = {
            "debian": "apt install -y",
            "ubuntu": "apt install -y",
            "python3": "`which pip3` install",
            "python": "`which pip` install",
        }

    def _os_install(self, package_file):
        """
        take in a dict return a string of docker build RUN directives
        one RUN per package type
        one package type per JSON key
        """
        packages = " ".join(json.load(package_file.open()))
        if packages:
            for packager in self.pkg_install_cmds:
                if packager in self.context.externalbasis:
                    installer = self.pkg_install_cmds[packager]
            return f"RUN    {installer} {packages}"
        else:
            return ""

    def _lang_install(self, package_file):
        """
        """
        packages_dict = json.load(package_file.open())
        install_command = ""
        if packages_dict:
            for lang in packages_dict:
                if lang in self.pkg_install_cmds:
                    packages = " ".join(packages_dict[lang])
                    installer = self.pkg_install_cmds[lang]
                    install_command = (
                        install_command + f"RUN    {installer} {packages}\n"
                    )
            return install_command
        else:
            return ""

    def pave_profile(self):
        """
        Usage:
          containment pave_profile
        """
        settings.personal_config.path.mkdir()
        json.dump(
            settings.personal_config.package_list,
            settings.personal_config.os_packages.open(mode="w"),
        )
        json.dump({}, settings.personal_config.lang_packages.open(mode="w"))
        settings.personal_config.projects.mkdir()

    def pave_project(self):
        """
        Usage:
          containment pave_project
        """
        settings.project_customization.path.mkdir()
        settings.project_customization.entrypoint.write_text(
            self.context.entrypoint_text
        )
        settings.project_customization.runfile.write_text(
            self.context.run_text
        )
        settings.project_customization.os_packages.write_text("[]")
        settings.project_customization.lang_packages.write_text("{}")
        self.write_dockerfile()

    def pave_community(self):
        """
        Usage:
          containment pave_community
        """
        settings.project_config.path.mkdir()
        settings.project_config.base.write_text(self.context.base_text)
        settings.project_config.os_packages.write_text("[]")
        settings.project_config.lang_packages.write_text("{}")

    def ensure_config(self):
        if not settings.project_config.path.is_dir():
            self.pave_community()
        if not settings.personal_config.path.is_dir():
            self.pave_profile()
        if not settings.project_customization.path.is_dir():
            self.pave_project()

    def write_dockerfile(self):
        """
        Usage:
          containment write_dockerfile
        """
        settings.project_customization.dockerfile.write_text(
            self._assemble_dockerfile()
        )

    def _assemble_dockerfile(self):
        return "\n".join(
            [
                settings.project_config.base.read_text(),
                self._os_install(settings.project_config.os_packages),
                self._os_install(settings.personal_config.os_packages),
                self._os_install(settings.project_customization.os_packages),
                self._lang_install(settings.project_config.lang_packages),
                self._lang_install(settings.personal_config.lang_packages),
                self._lang_install(
                    settings.project_customization.lang_packages
                ),
                self.context.project_adapter,
            ]
        )

    def build(self):
        """
        Usage:
          containment build
        """
        docker_build = docker.from_env().api.build
        build_actions = []
        for a in docker_build(
            str(settings.project_customization.path), tag=settings.tag
        ):
            build_actions.append(a)

    def run(self):
        """
        Usage:
          containment run
        """
        run_command = (
            settings.project_customization.runfile.read_text().split()
        )
        chmod_string = (
            "chmod +x "
            + settings.project_customization.runfile.absolute().as_posix()
        )
        subprocess.run(chmod_string.split())
        subprocess.run(
            run_command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
        )
