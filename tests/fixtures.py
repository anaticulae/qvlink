# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

import link
import tests

DOCUMENT = 'example'


@pytest.fixture
def example(testdir) -> str:
    root = str(testdir)
    todo = os.path.join(root, 'todo')
    os.makedirs(todo, exist_ok=True)
    ready = os.path.join(root, 'ready')
    os.makedirs(ready, exist_ok=True)

    source = tests.MINIMAL
    link.create_todo(
        source,
        filename='minimal.pdf',
        todopath=todo,
        todoname=DOCUMENT,
    )
    return root


@pytest.fixture
def broken(testdir) -> str:
    root = str(testdir)
    todo = os.path.join(root, 'todo')
    os.makedirs(todo, exist_ok=True)
    ready = os.path.join(root, 'ready')
    os.makedirs(ready, exist_ok=True)

    source = os.path.join(root, 'broken.pdf')
    utila.file_create(source, '')

    link.create_todo(
        source,
        filename='broken.pdf',
        todopath=todo,
        todoname=DOCUMENT,
    )
    return root
