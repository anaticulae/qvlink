# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import configo
import utila

import link
import link.state

PROGRESS_START = '000'


def start_progress(document: str):
    assert_state(link.ProcessState.NEW, document)

    path = link.state.inprogress(document)
    utila.file_create(path, PROGRESS_START)

    assert_state(link.ProcessState.STARTED, document)


def verify(document: str):
    assert_state(link.ProcessState.STARTED, document)

    todo = configo.todo()
    workspace = os.path.join(todo, document)
    pdf = os.path.join(workspace, document)

    result = utila.run(f'pdfinfo -i {pdf} -o {workspace}')
    assert result.returncode == utila.SUCCESS, (result.stderr + result.stdout)

    assert_state(
        [link.ProcessState.VERIFIED, link.ProcessState.INVALID],
        document,
    )


def start_analysis(document: str):
    assert_state(link.ProcessState.VERIFIED, document)

    todo = os.path.join(configo.todo(), document)
    fastview = os.path.join(todo, 'fastview')
    resultview = os.path.join(todo, 'result')

    os.makedirs(fastview)
    os.makedirs(resultview)

    assert_state(link.ProcessState.ANALYSIS, document)


def finish_fastview(document: str):
    assert_state(link.ProcessState.ANALYSIS, document)

    fastview = link.state.fastview_done(document)
    utila.file_create(fastview)


def finish_resultview(document: str):
    assert_state(link.ProcessState.ANALYSIS, document)

    assert link.current(document) == link.ProcessState.ANALYSIS
    resultview = link.state.resultview_done(document)
    utila.file_create(resultview)


def publish(document: str):
    assert_state(
        [link.ProcessState.ANALYSED, link.ProcessState.INVALID],
        document,
    )

    source = os.path.join(configo.todo(), document)
    destination = os.path.join(configo.ready(), document)
    os.makedirs(destination)
    assert os.path.exists(destination), destination

    utila.copy_content(source, destination, pattern='pdfinfo.json')
    utila.copy_content(source, destination, pattern='info.yaml')

    if utila.file_read(link.pdfinfo(document)) != '{}':
        # publis content only for valid pdf files
        utila.copy_content(
            link.state.fastview(document),
            os.path.join(destination, 'fastview'),
        )

        utila.copy_content(
            link.state.resultview(document),
            os.path.join(destination, 'result'),
        )

    utila.file_create(link.state.done(document))

    assert_state(link.ProcessState.PUBLISHED, document)


def assert_state(state, document):
    current = link.current(document)
    if not isinstance(state, list):
        state = [state]
    assert any([current == item for item in state]), current
