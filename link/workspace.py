# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import listdir
from os.path import exists
from os.path import join

import configo
import utila
from utila import logging_error

from link import JOB_FILE_NAME
from link import job_load


def scan(path: str):
    """Scan common space for jobs todo and done"""
    assert exists(path), path

    todo = configo.todo()
    ready = configo.ready()

    assert exists(todo), todo
    assert exists(ready), ready

    todos = []
    for item in listdir(todo):
        current = join(todo, item, JOB_FILE_NAME)
        if not exists(current):
            logging_error('Job does not exists: %s' % current)
            continue
        todos.append(job_load(current))

    readys = []
    for item in listdir(ready):
        current = join(ready, item, JOB_FILE_NAME)
        if not exists(current):
            logging_error('Job does not exists: %s' % current)
            continue
        readys.append(job_load(current))

    return todos, readys


def free_todo():
    """Generate file name which does not exists"""
    path = configo.todo()
    name = utila.tempname()
    while exists(join(path, name)):
        name = utila.tempname()
    return name
