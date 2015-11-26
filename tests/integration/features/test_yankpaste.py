# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2015 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
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

import pytest

from PyQt5.QtGui import QClipboard

import pytest_bdd as bdd


bdd.scenarios('yankpaste.feature')

# https://github.com/The-Compiler/qutebrowser/issues/1124#issuecomment-158073581
pytestmark = pytest.mark.qt_log_ignore(
    '^QXcbClipboard: SelectionRequest too old', extend=True)

@pytest.fixture(autouse=True)
def skip_with_broken_clipboard(qtbot, qapp):
    """The clipboard seems to be broken on some platforms (OS X Yosemite?).

    This skips the tests if this is the case.
    """
    clipboard = qapp.clipboard()

    with qtbot.waitSignal(clipboard.changed):
        clipboard.setText("Does this work?")

    if clipboard.text() != "Does this work?":
        pytest.skip("Clipboard seems to be broken on this platform.")
