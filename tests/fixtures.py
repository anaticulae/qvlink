# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import iamraw
import power
import protocol
import pytest
import utila

import link
import tests.patch

DOCUMENT = 'example'


@pytest.fixture
def example(testdir) -> str:
    todo = os.path.join(testdir.tmpdir, 'todo')
    os.makedirs(todo, exist_ok=True)
    ready = os.path.join(testdir.tmpdir, 'ready')
    os.makedirs(ready, exist_ok=True)
    # create todo
    link.create_todo(
        power.DOCU07_PDF,
        filename='minimal.pdf',
        todopath=todo,
        todoname=DOCUMENT,
    )
    return testdir.tmpdir


@pytest.fixture
def completed(example, monkeypatch) -> str:  # pylint:disable=W0621
    with complete(example, monkeypatch):
        pass
    with tests.patch.patch_todo(example, monkeypatch):
        ready = os.path.join(example, f'ready/{DOCUMENT}')
        yield ready


@pytest.fixture
def withfindings(completed):  # pylint:disable=W0621
    optimized = link.optimized(DOCUMENT, done=True)
    os.makedirs(optimized)
    findings = [
        iamraw.Finding(
            number=1337,
            location=iamraw.Location.from_page(2),
            solution=iamraw.Solution(),
        ),
        iamraw.Finding(
            number=1338,
            location=iamraw.Location.from_page(2),
            solution=iamraw.Solution(),
        ),
        iamraw.Finding(
            number=1339,
            location=iamraw.Location.from_page(1),
            solution=iamraw.Solution(),
        ),
        iamraw.Finding(
            number=1339,
            location=iamraw.Location.from_page(3),
            solution=iamraw.Solution(),
        ),
    ]
    protocol.write_grouped(findings, optimized)
    yield completed


@contextlib.contextmanager
def complete(example, monkeypatch):  # pylint:disable=W0621
    with tests.patch.patch_todo(example, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        link.start_analysis(DOCUMENT)
        link.finish_fastview(DOCUMENT)
        link.finish_resultview(DOCUMENT)
        link.publish(DOCUMENT)
        state = link.current(DOCUMENT)
        assert state == link.ProcessState.PUBLISHED
        yield


@pytest.fixture
def broken(testdir) -> str:
    todo = os.path.join(testdir.tmpdir, 'todo')
    os.makedirs(todo, exist_ok=True)
    ready = os.path.join(testdir.tmpdir, 'ready')
    os.makedirs(ready, exist_ok=True)

    source = os.path.join(testdir.tmpdir, 'broken.pdf')
    utila.file_create(source, '')

    link.create_todo(
        source,
        filename='broken.pdf',
        todopath=todo,
        todoname=DOCUMENT,
    )
    return testdir.tmpdir


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
        output = os.path.join(folder, link.JOBFILE_NAME)
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
        output = os.path.join(folder, link.JOBFILE_NAME)
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
