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


@pytest.fixture
def common(tmpdir):
    """Create common folder with `todo` and `ready` folder. Todo
    contains 3 elements, ready 2."""
    # TODO: USE FAKER TO GENERATE EXAMPLE JOBS
    todo = os.path.join(tmpdir, 'todo')
    ready = os.path.join(tmpdir, 'ready')
    os.makedirs(todo)
    os.makedirs(ready)

    for item in ['1234', '5555', '4321']:
        folder = os.path.join(todo, item)
        os.makedirs(folder)
        output = os.path.join(folder, link.JOB_FILE_NAME)
        result = link.JobInfo(
            title='Super Duper Masterarbeit',
            date='2019.04.01',
            name=item,
            result=None,
            owner=link.PUBLIC_OWNER,
        )
        dumped = link.dump_job(result)
        utila.file_create(output, dumped)

    for item in ['3333', '5555']:
        folder = os.path.join(ready, item)
        os.makedirs(folder)
        output = os.path.join(folder, link.JOB_FILE_NAME)
        result = link.JobInfo(
            title='Super Masterarbeit',
            date='2019.04.05',
            name=item,
            result=link.FindingStatus(10, 20, 30),
        )
        dumped = link.dump_job(result)
        utila.file_create(output, dumped)

    os.makedirs(os.path.join(todo, 'broken'))
    os.makedirs(os.path.join(ready, 'also_broken'))
    return tmpdir
