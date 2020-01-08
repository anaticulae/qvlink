# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
from contextlib import contextmanager
from os.path import exists
from os.path import join

from configo.directory import COMMON
from configo.directory import READY
from configo.directory import TODO

from link import ROOT

TEST_DATA = join(ROOT, 'tests/data')
assert exists(TEST_DATA), TEST_DATA

MINIMAL = join(TEST_DATA, 'minimal.pdf')
assert exists(MINIMAL), MINIMAL


@contextmanager
def patch_todo(directory, monkeypatch):
    environment = dict(os.environ)
    environment[COMMON] = directory
    environment[TODO] = join(directory, 'todo')
    environment[READY] = join(directory, 'ready')

    with monkeypatch.context() as context:
        context.setattr(os, 'environ', environment)
        yield
