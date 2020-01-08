# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

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


def test_state_verify_publish(example, monkeypatch):  # pylint:disable=W0621
    with tests.patch_todo(example, monkeypatch):
        link.start_progress(DOCUMENT)
        link.verify(DOCUMENT)
        link.start_analysis(DOCUMENT)
        link.finish_fastview(DOCUMENT)
        link.finish_resultview(DOCUMENT)
        link.publish(DOCUMENT)
        state = link.current(DOCUMENT)
    assert state == link.ProcessState.PUBLISHED

    ready = os.path.join(example, 'ready/example')
    assert os.path.join(ready), ready
    for item in ['fastview', 'result', 'done', 'pdfinfo.json', 'info.yaml']:
        assert os.path.exists(os.path.join(ready, item)), item
