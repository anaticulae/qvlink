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
    assert link.current(document) == link.ProcessState.NEW
    path = link.state.inprogress(document)
    utila.file_create(path, PROGRESS_START)
    assert link.current(document) == link.ProcessState.STARTED


def verify(document: str):
    assert link.current(document) == link.ProcessState.STARTED
    todo = configo.todo()
    workspace = os.path.join(todo, document)
    pdf = os.path.join(workspace, document)

    result = utila.run(f'pdfinfo -i {pdf} -o {workspace}')
    assert result.returncode == utila.SUCCESS, (result.stderr + result.stdout)
    assert link.current(document) == link.ProcessState.VERIFIED or \
                            link.current(document) == link.ProcessState.INVALID


def start_analysis(document: str):
    assert link.current(document) == link.ProcessState.VERIFIED
    todo = os.path.join(configo.todo(), document)
    fastview = os.path.join(todo, 'fastview')
    resultview = os.path.join(todo, 'result')

    os.makedirs(fastview)
    os.makedirs(resultview)
    assert link.current(document) == link.ProcessState.ANALYSIS


def finish_fastview(document: str):
    assert link.current(document) == link.ProcessState.ANALYSIS
    fastview = link.state.fastview_done(document)
    utila.file_create(fastview)


def finish_resultview(document: str):
    assert link.current(document) == link.ProcessState.ANALYSIS
    resultview = link.state.resultview_done(document)
    utila.file_create(resultview)


def publish(document: str):
    assert link.current(document) == link.ProcessState.ANALYSED
    source = os.path.join(configo.todo(), document)
    destination = os.path.join(configo.ready(), document)
    os.makedirs(destination)
    assert os.path.exists(destination), destination

    utila.copy_content(source, destination, pattern='pdfinfo.json')
    utila.copy_content(source, destination, pattern='info.yaml')

    utila.copy_content(
        link.state.fastview(document),
        os.path.join(destination, 'fastview'),
    )

    utila.copy_content(
        link.state.resultview(document),
        os.path.join(destination, 'result'),
    )

    utila.file_create(link.state.done(document))
    assert link.current(document) == link.ProcessState.PUBLISHED
