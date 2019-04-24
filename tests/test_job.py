# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from contextlib import contextmanager
from os import makedirs
from os.path import join

from configo.share import COMMON
from configo.share import READY
from configo.share import TODO
from pytest import fixture

from link import JOB_FILE_NAME
from link import JobInfo
from link import job_dump
from link import job_load
from link import scan


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


def test_common_folder(common, monkeypatch):
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
