# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2018 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Loader for qutebrowser extensions."""

import importlib.abc
import pkgutil
import types
import typing
import sys

import attr

from qutebrowser import components
from qutebrowser.utils import log


@attr.s
class ComponentInfo:

    name = attr.ib()  # type: str


def load_components() -> None:
    """Load everything from qutebrowser.components."""
    for info in walk_components():
        _load_component(info)


def walk_components() -> typing.Iterator[ComponentInfo]:
    """Yield ComponentInfo objects for all modules."""
    if hasattr(sys, 'frozen'):
        yield from _walk_pyinstaller()
    else:
        yield from _walk_normal()


def _walk_normal() -> typing.Iterator[ComponentInfo]:
    """Walk extensions when not using PyInstaller."""
    for _finder, name, ispkg in pkgutil.walk_packages(components.__path__):
        if ispkg:
            continue
        fullname = components.__name__ + '.' + name
        yield ComponentInfo(name=fullname)


def _walk_pyinstaller() -> typing.Iterator[ComponentInfo]:
    """Walk extensions when using PyInstaller.

    See https://github.com/pyinstaller/pyinstaller/issues/1905
    """
    toc = set()
    for importer in pkgutil.iter_importers('qutebrowser'):
        if hasattr(importer, 'toc'):
            toc |= importer.toc
    for name in toc:
        if name.startswith(components.__name__ + '.'):
            yield ComponentInfo(name=name)


def _load_component(info: ComponentInfo) -> types.ModuleType:
    log.extensions.debug("Importing {}".format(info.name))
    return importlib.import_module(info.name)
