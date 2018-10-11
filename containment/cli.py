#: -*- coding: utf-8 -*-
"""Contains the activate command and helper methods.

Functions:
    activate: Activate the given project. If no project name is given, activate
        the current directory.
"""

import json
import os
import pathlib
import subprocess
import sys
import time

import docker

from .types import ProjectId


class Community:
    def __init__(self):
        # COMMUNITY ACQUISITION
        self.path = pathlib.Path(os.getcwd())
        self.pathname = self.path.absolute().as_posix()
        self.containment = self.path.joinpath(".containment")
        self.base = self.containment.joinpath("base")
        self.os_packages = self.containment.joinpath("os_packages.json")
        self.lang_packages = self.containment.joinpath("lang_packages.json")


class Profile:
    def __init__(self):
        # PROFILE ACQUISITION
        self.home = os.environ["HOME"]
        self.path = pathlib.Path(self.home).joinpath(".containment")
        self.projects = self.path.joinpath("projects")
        self.package_list = [
            "vim",
            "tmux",
            "git",
            os.path.split(os.environ["SHELL"])[1],
        ]  # These are examples.
        self.os_packages = self.path.joinpath("os_packages.json")
        self.lang_packages = self.path.joinpath("lang_packages.json")


class Project:
    def __init__(self, cli):
        # PROJECT ACQUISITION
        self.path = cli.profile.projects.joinpath(cli.community.path.name)
        self.pathname = self.path.absolute().as_posix()
        self.tag = f"containment/{self.path.name}"
        self.dockerfile = self.path.joinpath("Dockerfile")
        self.runfile = self.path.joinpath("run_containment.sh")
        self.entrypoint = self.path.joinpath("entrypoint.sh")
        self.os_packages = self.path.joinpath("os_packages.json")
        self.lang_packages = self.path.joinpath("lang_packages.json")


class Context:
    def __init__(self, cli):
        # CONFIGURATION STRING VARIABLE VALUES
        self.user = os.environ["USER"]
        self.shell = os.environ["SHELL"]
        self.userid = subprocess.getoutput("id -u")
        self.dockergid = subprocess.getoutput("grep docker /etc/group").split(
            ":"
        )[2]
        # CONFIGURATION STRINGS
        self.project_adapter = f"""RUN     useradd -G docker --uid {self.userid} --home /home/{self.user} {self.user}
        RUN     echo {self.user} ALL=\(ALL\) NOPASSWD: ALL >> /etc/sudoers
        COPY    ./entrypoint.sh entrypoint.sh
        RUN     chmod +x entrypoint.sh"""
        self.entrypoint_text = f"""#!{self.shell}
        cd {cli.community.pathname}
        sudo sed -ie s/docker:x:[0-9]*:{self.user}/docker:x:{self.dockergid}:{self.user}/g /etc/group
        sudo usermod -s {self.shell} {self.user}
        exec {self.shell}"""
        try:
            self.ssh_auth_sock = os.environ["SSH_AUTH_SOCK"]
        except KeyError:
            self.ssh_auth_sock = ""
        if self.ssh_auth_sock:
            self.ssh_auth_sock_parent = pathlib.\
                                        Path(self.ssh_auth_sock).\
                                        parent.as_posix()
            self.run_text = f"""docker run -it \
                           -v /var/run/docker.sock:/var/run/docker.sock \
                           -v {cli.profile.home}:{cli.profile.home} \
                           -v {cli.community.pathname}:{cli.community.pathname} \
                           -v {self.ssh_auth_sock_parent} \
                           -e SSH_AUTH_SOCK={self.ssh_auth_sock} \
                           --entrypoint=/entrypoint.sh -u {self.user}:{self.dockergid} {cli.project.tag}:latest"""
        else:
            self.run_text = f"""docker run -it \
                           -v /var/run/docker.sock:/var/run/docker.sock \
                           -v {cli.profile.home}:{cli.profile.home} \
                           -v {cli.community.pathname}:{cli.community.pathname} \
                           --entrypoint=/entrypoint.sh -u {self.user}:{self.dockergid} {cli.project.tag}:latest"""

        self.externalbasis = ("ubuntu@latest")
        self.base_text = f"""FROM    {self.externalbasis}
        RUN     apt update && apt install -y sudo docker.io"""


class Command_Line_Interface:
    def __init__(self):

        self.community = Community()
        self.profile = Profile()
        self.project = Project(self)
        self.context = Context(self)
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
        self.profile.path.mkdir()
        json.dump(
            self.profile.package_list, self.profile.os_packages.open(mode="w")
        )
        json.dump({}, self.profile.lang_packages.open(mode="w"))
        self.profile.projects.mkdir()

    def pave_project(self):
        """
        Usage:
          containment pave_project
        """
        self.project.path.mkdir()
        self.project.entrypoint.write_text(self.context.entrypoint_text)
        self.project.runfile.write_text(self.context.run_text)
        self.project.os_packages.write_text("[]")
        self.project.lang_packages.write_text("{}")
        self.write_dockerfile()

    def pave_community(self):
        """
        Usage:
          containment pave_community
        """
        self.community.containment.mkdir()
        self.community.base.write_text(self.context.base_text)
        self.community.os_packages.write_text("[]")
        self.community.lang_packages.write_text("{}")

    def _assure_config(self):
        if not self.community.containment.is_dir():
            self.pave_community()
        if not self.profile.path.is_dir():
            self.pave_profile()
        if not self.project.path.is_dir():
            self.pave_project()

    def write_dockerfile(self):
        """
        Usage:
          containment write_dockerfile
        """
        self.project.dockerfile.write_text(self._assemble_dockerfile())

    def _assemble_dockerfile(self):
        return "\n".join(
            [
                self.community.base.read_text(),
                self._os_install(self.community.os_packages),
                self._os_install(self.profile.os_packages),
                self._os_install(self.project.os_packages),
                self._lang_install(self.community.lang_packages),
                self._lang_install(self.profile.lang_packages),
                self._lang_install(self.project.lang_packages),
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
        for a in docker_build(self.project.pathname, tag=self.project.tag):
            build_actions.append(a)

    def run(self):
        """
        Usage:
          containment run
        """
        run_command = self.project.runfile.read_text().split()
        chmod_string = "chmod +x " + self.project.runfile.absolute().as_posix()
        chmod_run = subprocess.run(chmod_string.split())
        run_subprocess = subprocess.run(
            run_command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
        )


def activate():
    """
    Usage:
      containment activate
    """
    # This is derived from the clone
    cli = Command_Line_Interface()
    cli._assure_config()
    cli.write_dockerfile()
    cli.build()
    cli.run()
