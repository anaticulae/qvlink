# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import configos.directory


@contextlib.contextmanager
def patch_todo(directory, monkeypatch):
    environment = dict(os.environ)
    environment[configos.directory.COMMON] = str(directory)
    environment[configos.directory.TODO] = str(os.path.join(directory, 'todo'))
    environment[configos.directory.READY] = str(os.path.join(
        directory, 'ready'))

    with monkeypatch.context() as context:
        context.setattr(os, 'environ', environment)
        yield
