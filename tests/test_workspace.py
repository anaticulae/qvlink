# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila

from link import free_todo


def test_free_todo(tmpdir, monkeypatch):
    """Generate the same random name twice. This happens not very often, but
    it can happen."""

    folder = iter(['test', 'test', 'ts'])

    def random_foldername():
        return next(folder)

    def todo():
        return tmpdir

    with monkeypatch.context() as context:
        context.setattr(utila, 'tempname', random_foldername)
        context.setattr(configo, 'todo', todo)

        # Create folder name, so the next call is already created
        os.makedirs(os.path.join(tmpdir, free_todo()))

        # test is already there, give me the next one
        assert free_todo() == 'ts'
