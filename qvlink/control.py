# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
import protoerror
import serializeraw
import utilo

import qvlink
import qvlink.state

PROGRESS_START = 0


def start_progress(document: str):
    assert_state(qvlink.ProcessState.NEW, document)

    qvlink.update_progress(document, PROGRESS_START)

    assert_state(qvlink.ProcessState.STARTED, document)


def verify(document: str):
    assert_state(qvlink.ProcessState.STARTED, document)

    todo = configos.todo()
    workspace = os.path.join(todo, document)
    pdf = os.path.join(workspace, document)

    result = utilo.run(f'pdflog -i {pdf} -o {workspace} --format=yaml')
    assert result.returncode == utilo.SUCCESS, (result.stderr + result.stdout)

    # TODO: ENABLE abel LATER
    # utilo.run(f'abel -i {pdf} -o {workspace}', expect=None)

    assert_state(
        [qvlink.ProcessState.VERIFIED, qvlink.ProcessState.INVALID],
        document,
    )


def start_analysis(document: str):
    assert_state(qvlink.ProcessState.VERIFIED, document)

    todo = os.path.join(configos.todo(), document)
    fastview = os.path.join(todo, 'fastview')
    resultview = os.path.join(todo, 'result')

    os.makedirs(fastview)
    os.makedirs(resultview)

    assert_state(qvlink.ProcessState.ANALYSIS, document)


def finish_fastview(document: str):
    assert_state(qvlink.ProcessState.ANALYSIS, document)

    fastview = qvlink.state.fastview_done(document)
    utilo.file_create(fastview)


def finish_resultview(document: str):
    assert_state(qvlink.ProcessState.ANALYSIS, document)

    assert qvlink.current(document) == qvlink.ProcessState.ANALYSIS
    resultview = qvlink.state.resultview_done(document)
    utilo.file_create(resultview)


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
        [qvlink.ProcessState.ANALYSED, qvlink.ProcessState.INVALID],
        document,
    )
    verbose = utilo.level_current() > utilo.Level.LOGGING
    source = os.path.join(configos.todo(), document)
    destination = os.path.join(configos.ready(), document)
    equal_location = source == destination
    if not equal_location:
        os.makedirs(destination)
    assert os.path.exists(destination), destination
    # count findings and update jobinfo.yaml
    init_jobcounter(source)
    if not equal_location:
        utilo.copy_content(source, destination, pattern=qvlink.PDFINFO_NAME)
        utilo.copy_content(source, destination, pattern=qvlink.JOBFILE_NAME)
    if isextracted(document):
        # decide if we encrypt result
        private = qvlink.private(document, done=False)
        # publish content only for valid pdf files
        utilo.log('copy fastview')
        utilo.copy_content(
            qvlink.fastview(document),
            qvlink.fastview(document, done=True),
            recursive=True,
            skip_equal=equal_location,
            verbose=verbose,
            ignore=skip_fastview,
            private=private,
        )
        utilo.log('copy resultview')
        utilo.copy_content(
            qvlink.resultview(document),
            qvlink.resultview(document, done=True),
            recursive=True,
            skip_equal=equal_location,
            verbose=verbose,
            ignore=skip_resultview,
            private=private,
        )
        # utilo.log('copy optimized')
        # utilo.copy_content(
        #     link.optimized(document),
        #     link.optimized(document, done=True),
        #     recursive=True,
        #     verbose=True,
        # )
    make_done(document)
    assert_state(qvlink.ProcessState.PUBLISHED, document)


def isextracted(documentid) -> bool:
    if utilo.file_read(qvlink.pdfinfo_path(documentid)) != '{}':
        return True
    return False


def write_optimized_findings(
    document: str,
    done: bool = False,
    active: set = None,
):
    optimized = qvlink.optimized(document, done=done)
    os.makedirs(optimized)
    utilo.log((f'load: {qvlink.resultview(document)} and '
               f'write optimized to: {optimized}'))
    findings = [
        pagefindings.content for pagefindings in protoerror.findings_from_path(
            path=qvlink.resultview(document),
            msgid=active,
        )
    ]
    findings = utilo.flatten(findings)
    findings = utilo.notnone(findings)
    protoerror.write_grouped(findings, optimized)


def init_jobcounter(source: str):
    """Count detected findings of analyzed document and write them to

    jobinfo yaml file.
    """
    optimized = os.path.join(source, 'result', '__optimized__')
    findings = []
    if utilo.exists(optimized):
        findings = serializeraw.load_grouped(optimized)
    else:
        utilo.error(f'no optimized findings: {optimized}')
    finding_count = len(utilo.flatten_content(findings))
    jobpath = os.path.join(source, qvlink.JOBFILE_NAME)
    current = qvlink.load_job(jobpath)
    current.result = qvlink.FindingStatus(finding_count, 0, 0)
    dumped = qvlink.dump_job(current)
    utilo.file_replace(jobpath, dumped)


def assert_state(state, document):
    current = qvlink.current(document)
    if not isinstance(state, list):
        state = [state]
    assert any(current == item for item in state), current


def make_done(documentid: str) -> bool:
    if qvlink.current(documentid) == qvlink.ProcessState.PUBLISHED:
        return False
    source = os.path.join(configos.todo(), documentid)
    destination = os.path.join(configos.ready(), documentid)
    equal_location = source == destination
    if equal_location:
        utilo.error('could not add done to equal location')
        return False
    jobinfo = qvlink.load_jobinfo(documentid, done=False)
    # set done flag
    jobinfo.done = True
    qvlink.save_job(jobinfo, done=True)
    utilo.file_create(qvlink.done(documentid))
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
    if qvlink.current(documentid) == qvlink.ProcessState.DELETED:
        return False

    todo_path = qvlink.todo(documentid)
    ready_path = qvlink.ready(documentid)

    if not (os.path.exists(todo_path) or os.path.exists(ready_path)):
        # document does not exists
        return False

    if os.path.exists(todo_path):
        utilo.file_create(qvlink.todo_deleted(documentid))

    if os.path.exists(ready_path):
        # processing is not completed(error or cancelled)
        utilo.file_create(qvlink.ready_deleted(documentid))

    return True
