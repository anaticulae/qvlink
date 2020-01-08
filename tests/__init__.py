# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import configo
from configo.directory import READY
from configo.directory import TODO

import link

TEST_DATA = os.path.join(link.ROOT, 'tests/data')
assert os.path.exists(TEST_DATA), TEST_DATA

MINIMAL = os.path.join(TEST_DATA, 'minimal.pdf')
assert os.path.exists(MINIMAL), MINIMAL


@contextlib.contextmanager
def patch_todo(directory, monkeypatch):
    environment = dict(os.environ)
    environment[configo.directory.COMMON] = directory
    environment[configo.directory.TODO] = os.path.join(directory, 'todo')
    environment[configo.directory.READY] = os.path.join(directory, 'ready')

    with monkeypatch.context() as context:
        context.setattr(os, 'environ', environment)
        yield
