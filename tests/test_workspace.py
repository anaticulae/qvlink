# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
from os.path import exists

import configo
import utila

import link.workspace
from link import create_todo
from link import free_todo
from tests import MINIMAL
from tests import patch_todo


def test_free_todo(tmpdir, monkeypatch):
    """Generate the same random name twice. This happens not very often, but
    it can happen."""

    folder = iter(['test', 'test', 'ts'])

    def random_foldername():
        return next(folder)

    def todo():
        return tmpdir

    with monkeypatch.context() as context:
        context.setattr(utila, 'tmpname', random_foldername)
        context.setattr(configo, 'todo', todo)

        # Create folder name, so the next call is already created
        os.makedirs(os.path.join(tmpdir, free_todo()))

        # test is already there, give me the next one
        assert free_todo() == 'ts'


def test_create_todo(tmpdir, monkeypatch):
    with patch_todo(tmpdir, monkeypatch):
        with open(MINIMAL, mode='rb') as fp:

            def patch(_):  # pylint:disable=W0613
                pass

            fp.save = patch
            created = create_todo(fp, 'testfile.pdf')

    assert exists(created), created


def test_sortable_date():
    # "%02d.%02d.%04d"
    expected = [
        '31.12.2019 05:10',
        '31.11.2019 12:12',
        '23.04.2019 05:11',
        '23.04.2019 05:10',
        '23.04.2019 04:10',
        '20.04.2019 05:10',
        '01.01.2019 05:10',
        '10.02.2018 05:10',
        '10.01.2018 05:10',
        '01.01.2018 05:10',
    ]

    result = [
        '10.01.2018 05:10',
        '20.04.2019 05:10',
        '10.02.2018 05:10',
        '01.01.2018 05:10',
        '31.12.2019 05:10',
        '23.04.2019 04:10',
        '23.04.2019 05:10',
        '23.04.2019 05:11',
        '01.01.2019 05:10',
        '31.11.2019 12:12',
    ]

    result = sorted(result, key=link.workspace.sortable_date, reverse=True)
    assert result == expected
