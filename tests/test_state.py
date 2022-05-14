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
import utila
import utilatest

import link
import tests
import tests.fixtures

DOCUMENT = tests.fixtures.DOCUMENT


def test_state_init(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.NEW


def test_state_start(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        link.control.start_progress(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.STARTED


@utilatest.longrun
def test_state_delete(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        link.control.start_progress(DOCUMENT)
        state = link.current(DOCUMENT)
        assert state == link.ProcessState.STARTED
        link.delete(DOCUMENT)
        state = link.current(DOCUMENT)
        assert state == link.ProcessState.DELETED
        # do not delete twice
        assert link.delete(DOCUMENT) is False  # pylint:disable=C2001


@utilatest.longrun
def test_state_failed(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        link.control.start_progress(DOCUMENT)
        link.fail(DOCUMENT)
        state = link.current(DOCUMENT)
        assert state == link.ProcessState.ERROR


@utilatest.longrun
def test_state_verify(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.VERIFIED


@utilatest.longrun
def test_state_verify_broken(broken, monkeypatch):
    with tests.patch.patch_todo(broken, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.INVALID


@utilatest.longrun
def test_state_verify_start_analysis(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        link.start_analysis(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.ANALYSIS


@utilatest.longrun
def test_state_verify_finish(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        link.start_analysis(DOCUMENT)
        link.finish_fastview(DOCUMENT)
        state = link.current(DOCUMENT)
        assert state == link.ProcessState.ANALYSIS
        link.finish_resultview(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.ANALYSED


@utilatest.longrun
def test_state_verify_publish(example, monkeypatch):
    with tests.fixtures.complete(example, monkeypatch):
        ready = os.path.join(example, 'ready/example')
        assert os.path.join(ready), ready
        for item in [
                'fastview', 'result', 'done', link.PDFINFO_NAME,
                link.JOBFILE_NAME
        ]:
            assert os.path.exists(os.path.join(ready, item)), item


@utilatest.longrun
def test_state_verify_result(example, monkeypatch):
    """Ensure that path refer to copied `ready` result instead of `todo`
    directory."""
    # TODO: THIS TEST SEEMS TO BE VERY USELESS
    done = True
    with tests.fixtures.complete(example, monkeypatch):
        fastview = link.fastview(DOCUMENT, done)
        resultview = link.resultview(DOCUMENT, done)
        fastview_done = link.fastview_done(DOCUMENT, done)
        resultview_done = link.resultview_done(DOCUMENT, done)
    for item in [fastview, resultview, fastview_done, resultview_done]:
        assert os.path.exists(item), item

    fastview = utila.forward_slash(str(fastview))
    resultview = utila.forward_slash(str(resultview))
    resultview_done = utila.forward_slash(str(resultview_done))
    fastview_done = utila.forward_slash(str(fastview_done))

    assert fastview.endswith('ready/example/fastview'), fastview
    assert resultview.endswith('ready/example/result'), resultview
    assert fastview_done.endswith('ready/example/fastview/done'), fastview_done
    assert resultview_done.endswith('ready/example/result/done'), resultview_done  # yapf:disable


def test_state_progress(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        link.control.start_progress(DOCUMENT)
        link.update_progress(DOCUMENT, 50.0)
        assert link.progress(DOCUMENT) == 50


def test_state_progress_step(example, monkeypatch):
    with tests.patch.patch_todo(example, monkeypatch):
        link.update_progress_step(DOCUMENT, 5, 15)
        assert link.progress(DOCUMENT) == 33
        link.update_progress_step(DOCUMENT, 15, 15)
        assert link.progress(DOCUMENT) == 100


def test_status_fromstr_error():
    with pytest.raises(ValueError):
        link.State.fromstr('')


@utilatest.longrun
def test_update_bookkeeping(withfindings):  # pylint:disable=W0613
    documentid = DOCUMENT
    assert not link.load_jobinfo(documentid).result.open
    assert link.update_bookkeeping(documentid)
    assert link.load_jobinfo(documentid).result.open == 4
