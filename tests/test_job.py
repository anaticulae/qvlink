# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import tests.patch


def test_dump_and_load():
    """Dump and load project an example configuration"""
    config = link.JobInfo(
        title='Name',
        date='Date',
        result=link.FindingStatus(10, 20, 30),
        name='AFC1337ACD',
    )
    dumped = link.dump_job(config)
    loaded = link.load_job(dumped)
    assert loaded == config


def test_common_folder(common, monkeypatch):
    with tests.patch.patch_todo(common, monkeypatch):
        jobs = link.collect_jobs(common)

    assert len(jobs[0] + jobs[1]) == 5, str(jobs)


def test_common_folder_owner_public(common, monkeypatch):
    with tests.patch.patch_todo(common, monkeypatch):
        jobs_todo, _ = link.collect_jobs(
            common,
            owner=link.PUBLIC_OWNER,
            skip_removed=True,  # increase test coverage
        )
    assert len(jobs_todo) == 3


def test_delete_job(common, monkeypatch):
    with tests.patch.patch_todo(common, monkeypatch):
        jobs_todo, _ = link.collect_jobs(
            common,
            owner=link.PUBLIC_OWNER,
            skip_removed=True,
        )
        assert len(jobs_todo) == 3
        # delete first todo job(set removed flag)
        link.delete(jobs_todo[0].name)
        jobs_todo, _ = link.collect_jobs(
            common,
            owner=link.PUBLIC_OWNER,
            skip_removed=True,
        )
        assert len(jobs_todo) == 2


def test_todo_count(common, monkeypatch):
    with tests.patch.patch_todo(common, monkeypatch):
        assert link.count_todo() == 3

    with tests.patch.patch_todo(common, monkeypatch):
        assert link.count_ready() == 2


def test_access_owner(common, monkeypatch):
    with tests.patch.patch_todo(common, monkeypatch):
        assert link.owner('1234', done=False) == link.PUBLIC_OWNER
        assert link.owner('3333') is None


DEBUG = """\
queuemo 1.1.1

# comment
rawmaker 2.0.0
"""


def test_load_debug():
    loaded = link.load_debug(DEBUG)
    assert loaded['rawmaker'] == '2.0.0'
    assert loaded['queuemo'] == '1.1.1'
