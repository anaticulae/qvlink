# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Document State Machine
======================

States
------

NEW
~~~

`upload_document`

* create new folder with document id and job description in todo directory

Action:

* NEW ->`schedule_process` -> STARTED

STARTED
~~~~~~~

* add `inprogress` file to signal that work is started
* start verification to check that thjere is an valid pdf document

Action:

* STARTED -> pdfinfo -> INVALID
* STARTED -> pdfinfo -> VERIFIED

INVALID
~~~~~~~

* Stop analysis and inform user that document can not be analysed

VERIFIED
~~~~~~~~

* wait for analysis

Action:

* VERIFIED -> `start_analysis` ANALYSIS

ANALYSIS
~~~~~~~~

`start_analysis`

* Start fast view
* Start result view
* Complete fast view (Signal?)
   * Create file done in fast view directory
* Complete result view (Signal?)
   * Create file done in result view directory

DONE
~~~~

If both ready files exists.

PUBLISHED
~~~~~~~~~

publish

* copy document todo to ready
* add publish file to signal that coping is ready
* delete/archive workspace

ERROR*
~~~~~~

* If some exceptions occurs, goto error mode
* Inform user about technical error

Path
----

`configo.todo` path where new documents are located

`configo.ready` path where completed documents are located

"""

import contextlib
import enum
import os

import configo
import iamraw
import protocol
import utila

import link.job


class ProcessState(enum.Enum):
    """Describe the state of current document analysis."""
    NEW = enum.auto()
    STARTED = enum.auto()
    VERIFIED = enum.auto()
    INVALID = enum.auto()
    ANALYSIS = enum.auto()
    ANALYSED = enum.auto()
    PUBLISHED = enum.auto()
    ERROR = enum.auto()
    DELETED = enum.auto()
    UNDEFINED = enum.auto()


class State(enum.Enum):
    WAITING = -1
    DONE = 0
    RUNNING = 1
    FAILED = 2

    @staticmethod
    def fromstr(item: str) -> 'State':
        """\
        >>> State.fromstr('2')
        <State.FAILED: 2>
        """
        with contextlib.suppress(ValueError):
            item = int(item)
        for state in State:
            if state.value == item:
                return state
        raise ValueError(f'could not create State from `{item}`')

    @staticmethod
    def fromstate(state: ProcessState) -> 'State':
        """\
        >>> State.fromstate(ProcessState.VERIFIED)
        <State.RUNNING: 1>
        """
        if state == ProcessState.NEW:
            return State.WAITING
        if state in (ProcessState.INVALID, ProcessState.ERROR):
            return State.FAILED
        if state == ProcessState.PUBLISHED:
            return State.DONE
        return State.RUNNING

    def __int__(self):
        """\
        >>> int(State.FAILED)
        2
        """
        return self.value


def current(documentid: str) -> ProcessState:  # pylint:disable=too-many-return-statements, too-many-locals, R1260
    """Determine state of process defined by `documentid` location.

    >>> assert current('doesnotexists') is None
    """
    if not document(documentid):
        # process does not exists
        return None

    publish = os.path.exists(os.path.join(ready(documentid), 'done'))
    pdfinfopath = pdfinfo(documentid)

    # Source and sink are the same. This is required when running queueumo
    # in single mode.
    equal_path = todo(documentid) == ready(documentid)
    new = all([
        os.path.exists(todo(documentid)),  # valid todo document folder
        os.path.exists(os.path.join(todo(documentid), documentid)),  # pdf file
        os.path.exists(os.path.join(todo(documentid), link.job.JOB_FILE_NAME)),
        (not os.path.exists(ready(documentid)) or equal_path),
        not os.path.exists(pdfinfopath),
        not inprogressed(documentid),
    ])
    started = all([
        inprogressed(documentid),
    ])
    verified = all([
        started,
        os.path.exists(pdfinfopath) and utila.file_read(pdfinfopath) != '{}',
    ])
    invalid = all([
        started,
        os.path.exists(pdfinfopath) and utila.file_read(pdfinfopath) == '{}',
    ])
    analysis = all([
        verified,
        os.path.exists(fastview(documentid)),
        os.path.exists(resultview(documentid)),
    ])
    analysed = all([
        analysis,
        os.path.exists(fastview_done(documentid)),
        os.path.exists(resultview_done(documentid)),
    ])
    published = all([
        publish,
    ])

    if deleted(documentid):
        return ProcessState.DELETED
    if failed(documentid):
        return ProcessState.ERROR
    if published:
        return ProcessState.PUBLISHED
    if analysed:
        return ProcessState.ANALYSED
    if analysis:
        return ProcessState.ANALYSIS
    if invalid:
        return ProcessState.INVALID
    if verified:
        return ProcessState.VERIFIED
    if started:
        return ProcessState.STARTED
    if new:
        return ProcessState.NEW
    return ProcessState.UNDEFINED


def todo(documentid: str, todopath=None) -> str:
    if not todopath:
        todopath = configo.todo()
    result = os.path.join(todopath, documentid)
    return result


def ready(documentid: str) -> str:
    result = os.path.join(configo.ready(), documentid)
    return result


def pdfinfo(documentid: str) -> str:
    source = todo(documentid)
    if os.path.exists(done_(documentid)):
        source = ready(documentid)
    result = os.path.join(source, link.PDFINFO_NAME)
    return result


def inprogress(documentid: str) -> str:
    result = os.path.join(todo(documentid), 'inprogress')
    return result


def inprogressed(documentid: str) -> bool:
    return os.path.exists(inprogress(documentid))


def fastview(documentid: str, done: bool = False) -> str:
    source = ready(documentid) if done else todo(documentid)
    return os.path.join(source, 'fastview')


def resultview(documentid: str, done: bool = False) -> str:
    source = ready(documentid) if done else todo(documentid)
    return os.path.join(source, 'result')


def optimized(documentid: str, done: bool = False) -> str:
    result = resultview(documentid, done=done)
    return os.path.join(result, '__optimized__')


def fastview_done(documentid: str, done: bool = False) -> str:
    result = os.path.join(fastview(documentid, done=done), 'done')
    return result


def resultview_done(documentid: str, done: bool = False) -> str:
    result = os.path.join(resultview(documentid, done=done), 'done')
    return result


def todo_deleted(documentid: str) -> str:
    return os.path.join(todo(documentid), 'deleted')


def ready_deleted(documentid: str) -> str:
    return os.path.join(ready(documentid), 'deleted')


def deleted(documentid: str) -> bool:
    if os.path.exists(todo_deleted(documentid)):
        return True
    if os.path.exists(ready_deleted(documentid)):
        return True
    return False


def done_(documentid: str) -> str:
    result = os.path.join(ready(documentid), 'done')
    return result


def owner(documentid: str, done: bool = True) -> str:
    info = load_jobinfo(documentid, done)
    return info.owner


def private(documentid: str) -> bool:
    return owner(documentid, done=False) != link.PUBLIC_OWNER


def progress(documentid: str) -> int:
    path = inprogress(documentid)
    if not os.path.exists(path):
        return -1
    result = utila.file_read(path)
    result = int(float(result))  # TODO: REPLACE WITH UTILA CODE
    return result


def fail(documentid: str, error: str = None):
    path = document(documentid)
    if not path:
        return
    path = os.path.join(path, 'failed')
    error = error or ''
    utila.file_replace(path, error)


def failed(documentid: str) -> bool:
    path = document(documentid)
    if not path:
        return None
    path = os.path.join(path, 'failed')
    return os.path.exists(path)


def load_jobinfo(documentid: str, done: bool = True) -> link.job.JobInfo:
    source = ready(documentid) if done else todo(documentid)
    path = os.path.join(source, link.JOB_FILE_NAME)
    loaded = link.load_job(path)
    return loaded


def document(documentid: str) -> str:
    """Access resource folder by `documentid`.

    Prefere ready over todo folder and return None if none of them
    exists.
    """
    if os.path.exists(ready(documentid)):
        return ready(documentid)
    if os.path.exists(todo(documentid)):
        return todo(documentid)
    return None


def update_progress(documentid: str, value: int):
    assert 0 <= value <= 100, f'invalid progress: {value}'
    path = inprogress(documentid)
    value = str(value).zfill(3)
    utila.file_replace(path, value)


def update_progress_step(documentid: str, value: int, maxvalue: int):
    assert 0 <= value <= maxvalue, f'invalid value: {value} <= {maxvalue}'
    percent = (value / maxvalue) * 100
    percent = utila.roundme(percent)
    update_progress(documentid, percent)


def update_bookkeeping(documentid: str) -> bool:
    path = link.optimized(documentid, done=True)
    findings = protocol.load_grouped(path)
    findings = utila.flatten([page.content for page in findings])
    opened, closed, excluded = 0, 0, 0
    for finding in findings:
        status = finding.solution.status
        if status == iamraw.ProblemStatus.OPEN:
            opened += 1
        elif status == iamraw.ProblemStatus.CLOSED:
            closed += 1
        else:
            excluded += 1
    job = link.load_jobinfo(documentid)
    job.result = link.FindingStatus(opened, closed, excluded)
    # update current job status
    utila.debug(f'update job information: {documentid}')
    link.save_job(job)
    return True
