# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import makedirs
from os.path import join

import utila
from pytest import fixture

import link
from link import JOB_FILE_NAME
from link import JobInfo
from link import collect_jobs
from link import count_ready
from link import count_todo
from link import dump_job
from link import load_job
from tests import patch_todo


def test_dump_and_load():
    """Dump and load project an example configuration"""
    config = JobInfo(
        title='Name',
        date='Date',
        result=link.FindingStatus(10, 20, 30),
        index=1337,
    )
    dumped = dump_job(config)
    loaded = load_job(dumped)
    assert loaded == config


def test_common_folder(common, monkeypatch):  # pylint:disable=W0621
    with patch_todo(common, monkeypatch):
        jobs = collect_jobs(common)

    assert len(jobs[0] + jobs[1]) == 5, str(jobs)


@fixture
def common(tmpdir):
    """Create common folder with `todo` and `ready` folder. Todo contains 3
    elements, ready 2."""
    todo = join(tmpdir, 'todo')
    ready = join(tmpdir, 'ready')
    makedirs(todo)
    makedirs(ready)

    for item in [1234, 5555, 4321]:
        folder = join(todo, '%d' % item)
        makedirs(folder)
        output = join(folder, JOB_FILE_NAME)
        result = JobInfo('Super Duper Masterarbeit', '2019.04.01', None, item)
        dumped = dump_job(result)
        utila.file_create(output, dumped)

    for item in [3333, 5555]:
        folder = join(ready, '%d' % item)
        makedirs(folder)
        output = join(folder, JOB_FILE_NAME)
        result = JobInfo('Super Masterarbeit', '2019.04.05', '95%', item)
        dumped = dump_job(result)
        utila.file_create(output, dumped)

    makedirs(join(todo, 'broken'))
    makedirs(join(ready, 'also_broken'))

    return tmpdir


def test_todo_count(common, monkeypatch):  # pylint:disable=W0621
    with patch_todo(common, monkeypatch):
        assert count_todo() == 3

    with patch_todo(common, monkeypatch):
        assert count_ready() == 2
