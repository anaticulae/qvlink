# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import protocol
import utila
import utila.logger

import link
import link.job
import link.state

PROGRESS_START = 0


def start_progress(document: str):
    assert_state(link.ProcessState.NEW, document)

    link.update_progress(document, PROGRESS_START)

    assert_state(link.ProcessState.STARTED, document)


def verify(document: str):
    assert_state(link.ProcessState.STARTED, document)

    todo = configo.todo()
    workspace = os.path.join(todo, document)
    pdf = os.path.join(workspace, document)

    result = utila.run(f'pdfinfo -i {pdf} -o {workspace} --format=yaml')
    assert result.returncode == utila.SUCCESS, (result.stderr + result.stdout)

    utila.run(f'abel -i {pdf} -o {workspace}', expect=None)

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


def publish(
    document: str,
    skip_fastview: callable = None,
    skip_resultview: callable = None,
):
    """\
    skip_fastview: do not copy file to public view
    skip_resultview: do not copy file to public view
    """
    assert_state(
        [link.ProcessState.ANALYSED, link.ProcessState.INVALID],
        document,
    )

    verbose = utila.logger.LEVEL > utila.Level.LOGGING

    source = os.path.join(configo.todo(), document)
    destination = os.path.join(configo.ready(), document)
    equal_location = source == destination
    if not equal_location:
        os.makedirs(destination)
    assert os.path.exists(destination), destination

    # count findings and update jobinfo.yaml
    init_jobcounter(source)

    if not equal_location:
        utila.copy_content(source, destination, pattern=link.PDFINFO_NAME)
        utila.copy_content(source, destination, pattern=link.JOBFILE_NAME)
    # decide if we encrypt result
    if utila.file_read(link.pdfinfo_path(document)) != '{}':
        private = link.private(document, done=False)
        # publish content only for valid pdf files
        utila.log('copy fastview')
        utila.copy_content(
            link.fastview(document),
            link.fastview(document, done=True),
            recursive=True,
            skip_equal=equal_location,
            verbose=verbose,
            ignore=skip_fastview,
            private=private,
        )

        utila.log('copy resultview')
        utila.copy_content(
            link.resultview(document),
            link.resultview(document, done=True),
            recursive=True,
            skip_equal=equal_location,
            verbose=verbose,
            ignore=skip_resultview,
            private=private,
        )

        # utila.log('copy optimized')
        # utila.copy_content(
        #     link.optimized(document),
        #     link.optimized(document, done=True),
        #     recursive=True,
        #     verbose=True,
        # )

    make_done(document)

    assert_state(link.ProcessState.PUBLISHED, document)


def write_optimized_findings(document: str, done: bool = False):
    optimized = link.optimized(document, done=done)
    os.makedirs(optimized)
    utila.log((f'load: {link.resultview(document)} and '
               f'write optimized to: {optimized}'))
    findings = [
        pagefindings.content for pagefindings in protocol.findings_from_path(
            link.resultview(document))
    ]
    findings = utila.flatten(findings)
    findings = utila.not_none(findings)
    protocol.write_grouped(findings, optimized)


def init_jobcounter(source: str):
    """Count detected findings of analyzed document and write them to
    jobinfo yaml file."""
    findings = protocol.findings_from_path(source)
    findings = utila.flatten([page.content for page in findings])
    jobpath = os.path.join(source, link.JOBFILE_NAME)
    current = link.load_job(jobpath)
    current.result = link.FindingStatus(len(findings), 0, 0)
    dumped = link.dump_job(current)
    utila.file_replace(jobpath, dumped)


def assert_state(state, document):
    current = link.current(document)
    if not isinstance(state, list):
        state = [state]
    assert any(current == item for item in state), current


def make_done(documentid: str) -> bool:
    if link.current(documentid) == link.ProcessState.PUBLISHED:
        return False
    source = os.path.join(configo.todo(), documentid)
    destination = os.path.join(configo.ready(), documentid)
    equal_location = source == destination
    if equal_location:
        utila.error('could not add done to equal location')
        return False
    jobinfo = link.load_jobinfo(documentid, done=False)
    # set done flag
    jobinfo.done = True
    link.save_job(jobinfo, done=True)
    utila.file_create(link.done(documentid))
    return True


def delete(documentid: str) -> bool:
    """Set deleting flag to mark fastview and resultview as deleted.

    This function works asynchronous. The content is removed later by
    `ResourceSyncScheduler`.

    Args:
        documentid(str): document id to identify document.
    Returns:
        True if deleting mark is successfully created.
        False if `document` is already marked as deleted.
    """
    if link.current(documentid) == link.ProcessState.DELETED:
        return False

    todo_path = link.todo(documentid)
    ready_path = link.ready(documentid)

    if not (os.path.exists(todo_path) or os.path.exists(ready_path)):
        # document does not exists
        return False

    if os.path.exists(todo_path):
        utila.file_create(link.todo_deleted(documentid))

    if os.path.exists(ready_path):
        # processing is not completed(error or cancelled)
        utila.file_create(link.ready_deleted(documentid))

    return True
