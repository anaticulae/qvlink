# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
* Info user about technical error

Path
----

`configo.todo` path where new documents are located

`configo.ready` path where completed documents are located

"""
import enum
import os

import configo
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


def current(documentid: str) -> ProcessState:  # pylint:disable=too-many-return-statements, too-many-locals
    """Determine state of process defined by `documentid` location.

    >>> assert current('doesnotexists') is None
    """
    if not (os.path.exists(todo(documentid)) or
            os.path.exists(ready(documentid))):
        # process does not exists
        return None
    inprogressed = os.path.exists(inprogress(documentid))

    publish = os.path.exists(os.path.join(ready(documentid), 'done'))
    pdfinfopath = pdfinfo(documentid)

    new = all([
        os.path.exists(todo(documentid)),  # valid todo document folder
        os.path.exists(os.path.join(todo(documentid), documentid)),  # pdf file
        os.path.exists(os.path.join(todo(documentid), link.job.JOB_FILE_NAME)),
        not os.path.exists(ready(documentid)),
        not os.path.exists(pdfinfopath),
        not inprogressed,
    ])
    started = all([
        inprogressed,
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
    deleted = any([
        os.path.exists(ready_deleted(documentid)),
        os.path.exists(todo_deleted(documentid)),
    ])

    if deleted:
        return ProcessState.DELETED
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


def todo(documentid: str) -> str:
    result = os.path.join(configo.todo(), documentid)
    return result


def ready(documentid: str) -> str:
    result = os.path.join(configo.ready(), documentid)
    return result


def pdfinfo(documentid: str) -> str:
    source = todo(documentid)
    if os.path.exists(done_(documentid)):
        source = ready(documentid)
    result = os.path.join(source, 'pdfinfo.json')
    return result


def inprogress(documentid: str) -> str:
    result = os.path.join(todo(documentid), 'inprogress')
    return result


def fastview(documentid: str) -> str:
    source = todo(documentid)
    if os.path.exists(done(documentid)):
        source = ready(documentid)
    return os.path.join(source, 'fastview')


def resultview(documentid: str) -> str:
    source = todo(documentid)
    if os.path.exists(done(documentid)):
        source = ready(documentid)
    return os.path.join(source, 'result')


def fastview_done(documentid: str) -> str:
    result = os.path.join(fastview(documentid), 'done')
    return result


def resultview_done(documentid: str) -> str:
    result = os.path.join(resultview(documentid), 'done')
    return result


def todo_deleted(documentid: str) -> str:
    return os.path.join(todo(documentid), 'deleted')


def ready_deleted(documentid: str) -> str:
    return os.path.join(ready(documentid), 'deleted')


def done_(documentid: str) -> str:
    result = os.path.join(ready(documentid), 'done')
    return result


def document(documentid: str) -> str:
    """Access resource folder by `documentid`. Prefere ready over todo
    folder and return None if none of them exists."""
    if os.path.exists(ready(documentid)):
        return ready(documentid)
    if os.path.exists(todo(documentid)):
        return todo(documentid)
    return None
