# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from contextlib import contextmanager
from os.path import exists
from os.path import join

from configo.share import COMMON
from configo.share import READY
from configo.share import TODO

from link import ROOT

TEST_DATA = join(ROOT, 'tests/data')
assert exists(TEST_DATA), TEST_DATA

MINIMAL = join(TEST_DATA, 'minimal.pdf')
assert exists(MINIMAL), MINIMAL


@contextmanager
def patch_todo(directory, monkeypatch):
    import os
    with monkeypatch.context() as context:
        # Remove all environment vars
        context.setattr(
            os, 'environ', {
                COMMON: directory,
                TODO: join(directory, 'todo'),
                READY: join(directory, 'ready'),
            })
        yield
