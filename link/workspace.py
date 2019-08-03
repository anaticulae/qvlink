# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from os import listdir
from os import makedirs
from os.path import exists
from os.path import join

import configo
import utila
from utila import error
from utila import today

from link import JOB_FILE_NAME
from link import JobInfo
from link import job_dump
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
            error('Job does not exists: %s' % current)
            continue
        todos.append(job_load(current))

    readys = []
    for item in listdir(ready):
        current = join(ready, item, JOB_FILE_NAME)
        if not exists(current):
            error('Job does not exists: %s' % current)
            continue
        readys.append(job_load(current))

    return todos, readys


def free_todo():
    """Generate file name which does not exists"""
    path = configo.todo()
    name = utila.tmpname()
    while exists(join(path, name)):
        name = utila.tmpname()
    return name


def create_todo(file, filename):
    """Create working folder, add info.yaml and write `file` to todo dir"""
    name = free_todo()
    todo_path = configo.todo()

    path = join(todo_path, name)
    assert not exists(path)

    makedirs(path)
    file_path = join(path, name)
    info_path = join(path, JOB_FILE_NAME)
    # Copy provied file to todo location
    file.save(file_path)

    # filename = secure_filename(file.filename)
    # Create job information
    job = JobInfo(title=filename, date=today(), index=name)
    job_dump(info_path, job)

    return path
