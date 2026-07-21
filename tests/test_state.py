# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utilo
import utilotest

import qvlink
import tests
import tests.fixtures

DOCUMENT = tests.fixtures.DOCUMENT


def test_state_init(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        state = qvlink.current(DOCUMENT)
    assert state == qvlink.ProcessState.NEW


def test_state_start(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        qvlink.control.start_progress(DOCUMENT)
        state = qvlink.current(DOCUMENT)
    assert state == qvlink.ProcessState.STARTED


@utilotest.longrun
def test_state_delete(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        qvlink.control.start_progress(DOCUMENT)
        state = qvlink.current(DOCUMENT)
        assert state == qvlink.ProcessState.STARTED
        qvlink.delete(DOCUMENT)
        state = qvlink.current(DOCUMENT)
        assert state == qvlink.ProcessState.DELETED
        # do not delete twice
        assert qvlink.delete(DOCUMENT) is False  # pylint:disable=C2001


@utilotest.longrun
def test_state_failed(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        qvlink.control.start_progress(DOCUMENT)
        qvlink.fail(DOCUMENT)
        state = qvlink.current(DOCUMENT)
        assert state == qvlink.ProcessState.ERROR


@utilotest.longrun
def test_state_verify(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        qvlink.start_progress(DOCUMENT)
        qvlink.verify(DOCUMENT)
        state = qvlink.current(DOCUMENT)
    assert state == qvlink.ProcessState.VERIFIED


@utilotest.longrun
def test_state_verify_broken(broken, monkeypatch):
    with tests.patch.patch_todo(broken, monkeypatch):
        qvlink.start_progress(DOCUMENT)
        qvlink.verify(DOCUMENT)
        state = qvlink.current(DOCUMENT)
    assert state == qvlink.ProcessState.INVALID


@utilotest.longrun
def test_state_verify_start_analysis(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        qvlink.start_progress(DOCUMENT)
        qvlink.verify(DOCUMENT)
        qvlink.start_analysis(DOCUMENT)
        state = qvlink.current(DOCUMENT)
    assert state == qvlink.ProcessState.ANALYSIS


@utilotest.longrun
def test_state_verify_finish(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        qvlink.start_progress(DOCUMENT)
        qvlink.verify(DOCUMENT)
        qvlink.start_analysis(DOCUMENT)
        qvlink.finish_fastview(DOCUMENT)
        state = qvlink.current(DOCUMENT)
        assert state == qvlink.ProcessState.ANALYSIS
        qvlink.finish_resultview(DOCUMENT)
        state = qvlink.current(DOCUMENT)
    assert state == qvlink.ProcessState.ANALYSED


@utilotest.longrun
def test_state_verify_publish(example, monkeypatch):
    with tests.fixtures.complete(example, monkeypatch):
        ready = os.path.join(example, 'ready/example')
        assert os.path.join(ready), ready
        for item in ('fastview', 'result', 'done', qvlink.PDFINFO_NAME,
                     qvlink.JOBFILE_NAME):
            assert os.path.exists(os.path.join(ready, item)), item


@utilotest.longrun
def test_state_verify_result(example, monkeypatch):
    """Ensure that path refer to copied `ready` result instead of `todo`
    directory."""
    # TODO: THIS TEST SEEMS TO BE VERY USELESS
    done = True
    with tests.fixtures.complete(example, monkeypatch):
        fastview = qvlink.fastview(DOCUMENT, done)
        resultview = qvlink.resultview(DOCUMENT, done)
        fastview_done = qvlink.fastview_done(DOCUMENT, done)
        resultview_done = qvlink.resultview_done(DOCUMENT, done)
    for item in (fastview, resultview, fastview_done, resultview_done):
        assert os.path.exists(item), item

    fastview = utilo.forward_slash(str(fastview))
    resultview = utilo.forward_slash(str(resultview))
    resultview_done = utilo.forward_slash(str(resultview_done))
    fastview_done = utilo.forward_slash(str(fastview_done))

    assert fastview.endswith('ready/example/fastview'), fastview
    assert resultview.endswith('ready/example/result'), resultview
    assert fastview_done.endswith('ready/example/fastview/done'), fastview_done
    assert resultview_done.endswith('ready/example/result/done'), resultview_done  # yapf:disable


def test_state_progress(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        qvlink.control.start_progress(DOCUMENT)
        qvlink.update_progress(DOCUMENT, 50.0)
        assert qvlink.progress(DOCUMENT) == 50


def test_state_progress_step(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        qvlink.update_progress_step(DOCUMENT, 5, 15)
        assert qvlink.progress(DOCUMENT) == 33
        qvlink.update_progress_step(DOCUMENT, 15, 15)
        assert qvlink.progress(DOCUMENT) == 100


def test_status_fromstr_error():
    with pytest.raises(ValueError):
        qvlink.State.fromstr('')


@utilotest.longrun
def test_update_bookkeeping(withfindings):  # pylint:disable=W0613
    documentid = DOCUMENT
    assert not qvlink.load_jobinfo(documentid).result.open
    assert qvlink.update_bookkeeping(documentid)
    assert qvlink.load_jobinfo(documentid).result.open == 4
