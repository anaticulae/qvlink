# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import configos
import hoverpower
import utilo

import qvlink
import tests


def test_free_todo(tmpdir, monkeypatch):
    """Generate the same random name twice. This happens not very often,
    but it can happen."""

    folder = iter(['test', 'test', 'ts'])

    def random_foldername(width=None):  # pylint:disable=W0613
        return next(folder)

    def todo():
        return tmpdir

    with monkeypatch.context() as context:
        context.setattr(utilo, 'tmpname', random_foldername)
        context.setattr(configos, 'todo', todo)

        # Create folder name, so the next call is already created
        os.makedirs(os.path.join(tmpdir, qvlink.find_free_todo()))

        # test is already there, give me the next one
        assert qvlink.find_free_todo() == 'ts'


def test_create_todo(tmpdir, monkeypatch):
    with tests.patch.patch_todo(tmpdir, monkeypatch):

        class SaveMock:

            def save(self, _):  # pylint:disable=W0613
                pass

        created = qvlink.create_todo(SaveMock(), 'testfile.pdf')
    assert os.path.exists(created), created


def test_create_todo_pathandname(testdir):
    created = qvlink.create_todo(
        hoverpower.DOCU007_PDF,
        'testfile.pdf',
        testdir.tmpdir,
        'helmut',
    )
    assert os.path.exists(created), created


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

    result = sorted(result, key=qvlink.sortable_date, reverse=True)
    assert result == expected


def test_load_documents(common, monkeypatch):
    """Verify that loading documents by state works correctly.

    1. Create todo(fixture:common)
    2. Verify that creation works
    3. Start single document
    4. Count state after start
    """
    # 2 todos, two are already solved
    new = 2
    with tests.patch.patch_todo(common, monkeypatch):
        load_documents = functools.partial(
            qvlink.load_documents,
            common=configos.share(),
            owner=None,
        )
        documents = load_documents(state=None)
        assert len(documents) == 4
        done = load_documents(state=qvlink.State.DONE)
        assert len(done) == 2
        # no documents in processing
        running = load_documents(state=qvlink.State.RUNNING)
        assert not running
        # 2 new documents wait for processing
        waiting = load_documents(state=qvlink.State.WAITING)
        assert len(waiting) == new
        documentid = waiting[0].get('name')
        # start first document
        qvlink.start_progress(document=documentid)
        waiting = load_documents(state=qvlink.State.WAITING)
        # one document is started
        assert len(waiting) == new - 1
        running = load_documents(state=qvlink.State.RUNNING)
        assert len(running) == 1
