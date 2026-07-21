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

import hoverpower
import iamraw
import protoerror
import pytest
import utilo

import qvlink
import tests.patch

DOCUMENT = 'example'


@pytest.fixture
def example(testdir) -> str:
    if not utilo.exists(hoverpower.DOCU007_PDF):
        pytest.skip(f'Download: {hoverpower.DOCU007_PDF}')
    todo = os.path.join(testdir.tmpdir, 'todo')
    os.makedirs(todo, exist_ok=True)
    ready = os.path.join(testdir.tmpdir, 'ready')
    os.makedirs(ready, exist_ok=True)
    # create todo
    qvlink.create_todo(
        hoverpower.DOCU007_PDF,
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
    optimized = qvlink.optimized(DOCUMENT, done=True)
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
    protoerror.write_grouped(findings, optimized)
    yield completed


@contextlib.contextmanager
def complete(example, monkeypatch):  # pylint:disable=W0621
    with tests.patch.patch_todo(example, monkeypatch):
        qvlink.start_progress(DOCUMENT)
        qvlink.verify(DOCUMENT)
        qvlink.start_analysis(DOCUMENT)
        qvlink.finish_fastview(DOCUMENT)
        qvlink.finish_resultview(DOCUMENT)
        qvlink.publish(DOCUMENT)
        state = qvlink.current(DOCUMENT)
        assert state == qvlink.ProcessState.PUBLISHED
        yield


@pytest.fixture
def broken(testdir) -> str:
    todo = os.path.join(testdir.tmpdir, 'todo')
    os.makedirs(todo, exist_ok=True)
    ready = os.path.join(testdir.tmpdir, 'ready')
    os.makedirs(ready, exist_ok=True)

    source = os.path.join(testdir.tmpdir, 'broken.pdf')
    utilo.file_create(source, '')

    qvlink.create_todo(
        source,
        filename='broken.pdf',
        todopath=todo,
        todoname=DOCUMENT,
    )
    return testdir.tmpdir


THESIS = [
    ('Helmuts Arbeit', '2022.01.05'),
    ('Frank MasterArbeit', '2019.01.05'),
    # todo
    ('Theos Studienarbeit', '2021.04.08'),
    # done
    ('Theos Studienarbeit', '2021.04.08'),
    ('Leas Abschlussarbeit', '2022.01.05'),
]


@pytest.fixture
def common(tmpdir):
    """Create common folder with `todo` and `ready` folder.

    Todo contains 3 elements, ready 2.
    """
    thesis = iter(THESIS)
    # TODO: USE FAKER TO GENERATE EXAMPLE JOBS
    todo = tmpdir.join('todo')
    ready = tmpdir.join('ready')
    todo.mkdir()
    ready.mkdir()
    # create todo
    for item in '1234 4321 5555'.split():
        folder = todo.join(item)
        folder.mkdir()
        output = folder.join(qvlink.JOBFILE_NAME)
        title, date = next(thesis)
        result = qvlink.JobInfo(
            title=title,
            date=date,
            name=item,
            result=None,
            owner=qvlink.PUBLIC_OWNER,
        )
        dumped = qvlink.dump_job(result)
        utilo.file_create(output, dumped)
        utilo.file_create_binary(folder.join(item), b'pdf content')
    todo.join('broken').mkdir()
    # create done
    for item in '5555 3333'.split():
        folder = ready.join(item)
        folder.mkdir()
        output = folder.join(qvlink.JOBFILE_NAME)
        title, date = next(thesis)
        result = qvlink.JobInfo(
            title=title,
            date=date,
            name=item,
            result=qvlink.FindingStatus(10, 20, 30),
        )
        dumped = qvlink.dump_job(result)
        utilo.file_create(output, dumped)
        # complete job
        utilo.file_create(folder.join('done'))
    ready.join('also_broken').mkdir()
    return tmpdir
