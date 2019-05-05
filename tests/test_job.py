# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import makedirs
from os.path import join

from pytest import fixture

from link import JOB_FILE_NAME
from link import JobInfo
from link import job_dump
from link import job_load
from link import ready_count
from link import scan
from link import todo_count
from tests import patch_todo


def test_dump_and_load(tmpdir):
    """Dump and load project an example configuration"""
    config = JobInfo(
        title='Name',
        date='Date',
        result='Result',
        index=1337,
    )

    path = join(tmpdir, 'configuration.yaml')
    job_dump(path, config)
    loaded = job_load(path)

    assert loaded == config


def test_common_folder(common, monkeypatch):  # pylint:disable=W0621
    with patch_todo(common, monkeypatch):
        jobs = scan(common)

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
        job_dump(output, result)

    for item in [3333, 5555]:
        folder = join(ready, '%d' % item)
        makedirs(folder)
        output = join(folder, JOB_FILE_NAME)
        result = JobInfo('Super Masterarbeit', '2019.04.05', '95%', item)
        job_dump(output, result)

    makedirs(join(todo, 'broken'))
    makedirs(join(ready, 'also_broken'))

    return tmpdir


def test_todo_count(common, monkeypatch):  # pylint:disable=W0621
    with patch_todo(common, monkeypatch):
        assert todo_count() == 3

    with patch_todo(common, monkeypatch):
        assert ready_count() == 2
