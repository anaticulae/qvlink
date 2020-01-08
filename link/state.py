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
import json
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
    UNDEFINED = enum.auto()


def current(document: str) -> ProcessState:  # pylint:disable=too-many-return-statements, too-many-locals
    todo = os.path.join(configo.todo(), document)
    ready = os.path.join(configo.ready(), document)

    pdfinfo = os.path.join(todo, 'pdfinfo.json')
    inprogressed = os.path.exists(inprogress(document))

    publish = os.path.exists(os.path.join(ready, 'done'))

    new = all([
        os.path.exists(todo),  # valid todo document folder
        os.path.exists(os.path.join(todo, document)),  # valid document
        os.path.exists(os.path.join(todo, link.job.FILE_NAME)),
        not os.path.exists(ready),
        not os.path.exists(pdfinfo),
        not inprogressed,
    ])
    started = all([
        inprogressed,
    ])
    verified = all([
        started,
        os.path.exists(pdfinfo) and json.loads(utila.file_read(pdfinfo)) != {},
    ])
    invalid = all([
        started,
        os.path.exists(pdfinfo) and json.loads(utila.file_read(pdfinfo)) == {},
    ])
    analysis = all([
        verified,
        os.path.exists(fastview(document)),
        os.path.exists(resultview(document)),
    ])
    analysed = all([
        analysis,
        os.path.exists(fastview_done(document)),
        os.path.exists(resultview_done(document)),
    ])
    published = all([
        publish,
    ])

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


def inprogress(document: str) -> str:
    todo = os.path.join(configo.todo(), document)
    result = os.path.join(todo, 'inprogress')
    return result


def fastview(document: str) -> str:
    todo = os.path.join(configo.todo(), document)
    result = os.path.join(todo, 'fastview')
    return result


def resultview(document: str) -> str:
    todo = os.path.join(configo.todo(), document)
    result = os.path.join(todo, 'result')
    return result


def fastview_done(document: str) -> str:
    result = os.path.join(fastview(document), 'done')
    return result


def resultview_done(document: str) -> str:
    result = os.path.join(resultview(document), 'done')
    return result


def done(document: str) -> str:
    ready = os.path.join(configo.ready(), document)
    result = os.path.join(ready, 'done')
    return result
