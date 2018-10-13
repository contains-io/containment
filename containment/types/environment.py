# -*- coding: utf-8 -*-
import os

from typet import Object
from typet import String


class EnvironmentVariable(Object):
    name: String[1:]

    @property
    def value(self):
        return os.environ.get(self.name)
