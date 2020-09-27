# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import utila

import link
import tests
# pylint:disable=W0611
from tests.fixtures import DOCUMENT
from tests.fixtures import broken
from tests.fixtures import example


def test_state_init(example, monkeypatch):  # pylint:disable=W0621
    with tests.patch_todo(example, monkeypatch):
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.NEW


def test_state_start(example, monkeypatch):  # pylint:disable=W0621
    with tests.patch_todo(example, monkeypatch):
        link.control.start_progress(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.STARTED


def test_state_verify(example, monkeypatch):  # pylint:disable=W0621
    with tests.patch_todo(example, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.VERIFIED


def test_state_verify_broken(broken, monkeypatch):  # pylint:disable=W0621
    with tests.patch_todo(broken, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.INVALID


def test_state_verify_start_analysis(example, monkeypatch):  # pylint:disable=W0621
    with tests.patch_todo(example, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        link.start_analysis(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.ANALYSIS


def test_state_verify_finish(example, monkeypatch):  # pylint:disable=W0621
    with tests.patch_todo(example, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        link.start_analysis(DOCUMENT)
        link.finish_fastview(DOCUMENT)
        state = link.current(DOCUMENT)
        assert state == link.ProcessState.ANALYSIS
        link.finish_resultview(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.ANALYSED


@contextlib.contextmanager
def completed(example, monkeypatch):  # pylint:disable=W0621
    with tests.patch_todo(example, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        link.start_analysis(DOCUMENT)
        link.finish_fastview(DOCUMENT)
        link.finish_resultview(DOCUMENT)
        link.publish(DOCUMENT)
        state = link.current(DOCUMENT)
        assert state == link.ProcessState.PUBLISHED
        yield


def test_state_verify_publish(example, monkeypatch):  # pylint:disable=W0621
    with completed(example, monkeypatch):
        ready = os.path.join(example, 'ready/example')
        assert os.path.join(ready), ready
        for item in ['fastview', 'result', 'done', 'pdfinfo.json', 'info.yaml']:
            assert os.path.exists(os.path.join(ready, item)), item


def test_state_verify_result(example, monkeypatch):  # pylint:disable=W0621
    """Ensure that path refer to copied `ready` result instead of `todo`
    directory."""
    # TODO: THIS TEST SEEMS TO BE VERY USELESS
    done = True
    with completed(example, monkeypatch):
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
    assert resultview_done.endswith('ready/example/result/done'), resultview_done # yapf:disable
