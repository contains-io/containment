# -*- coding: utf-8 -*-
class ContainmentException(Exception):
    pass


class NoSuchGroup(ContainmentException):
    pass


class DockerGroupMissing(NoSuchGroup):
    pass
