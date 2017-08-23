# -*- coding: utf-8 -*-
# Cardboardlint is a cheap lint solution for pull requests.
# Copyright (C) 2011-2017 The Cardboardlint Development Team
#
# This file is part of Cardboardlint.
#
# Cardboardlint is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Cardboardlint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --
"""Test some common functions."""


from nose.tools import assert_raises

from cardboardlint.common import get_offset_step, filter_selection
from cardboardlint.linter_cppcheck import linter_cppcheck
from cardboardlint.linter_pylint import linter_pylint


def test_offset_step():
    assert get_offset_step('') == (0, 1)
    assert get_offset_step('1/1') == (0, 1)
    assert get_offset_step('1/2') == (0, 2)
    assert get_offset_step('2/2') == (1, 2)
    assert get_offset_step('1/3') == (0, 3)
    assert get_offset_step('2/3') == (1, 3)
    assert get_offset_step('3/3') == (2, 3)

    assert_raises(ValueError, get_offset_step, '5')
    assert_raises(ValueError, get_offset_step, '5/5/6')
    assert_raises(ValueError, get_offset_step, '0/0')
    assert_raises(ValueError, get_offset_step, '1/0')
    assert_raises(ValueError, get_offset_step, '3/2')
    assert_raises(ValueError, get_offset_step, '-1/2')


def test_filter_selection():
    configs = [
        ('pylint', linter_pylint, {'pylintrc': '1'}),
        ('pylint', linter_pylint, {'pylintrc': '2'}),
        # The following may be a bad idea. cppcheck combines info from related files
        # when provided. (This is just used here for testing the filter_selection function.)
        ('cppcheck', linter_cppcheck, {'include': ['*.h.in']}),
        ('cppcheck', linter_cppcheck, {'include': ['*.h']}),
        ('cppcheck', linter_cppcheck, {'include': ['*.cpp']}),
    ]
    assert filter_selection(configs, None) == configs
    assert filter_selection(configs, '') == configs
    assert filter_selection(configs, 'all') == configs
    assert filter_selection(configs, 'cppcheck') == [configs[2], configs[3], configs[4]]
    assert filter_selection(configs, 'pylint') == [configs[0], configs[1]]
    assert filter_selection(configs, 'static') == [configs[2], configs[3], configs[4]]
    assert filter_selection(configs, 'dynamic') == [configs[0], configs[1]]
    assert filter_selection(configs, 'all1/2') == [configs[0], configs[2], configs[4]]
    assert filter_selection(configs, 'all2/2') == [configs[1], configs[3]]
    assert filter_selection(configs, 'all1/3') == [configs[0], configs[3]]
    assert filter_selection(configs, 'all2/3') == [configs[1], configs[4]]
    assert filter_selection(configs, 'all3/3') == [configs[2]]
    assert filter_selection(configs, 'static1/2') == [configs[2], configs[4]]
    assert filter_selection(configs, 'static2/2') == [configs[3]]
    assert filter_selection(configs, 'dynamic1/2') == [configs[0]]
    assert filter_selection(configs, 'dynamic2/2') == [configs[1]]
    assert filter_selection(configs, 'dynamic1/3') == [configs[0]]
    assert filter_selection(configs, 'dynamic2/3') == [configs[1]]
    assert filter_selection(configs, 'dynamic3/3') == []