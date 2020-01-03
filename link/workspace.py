# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila

import link


def scan(path: str):
    """Scan common space for jobs todo and done"""
    assert os.path.exists(path), path

    todo = configo.todo()
    ready = configo.ready()

    assert os.path.exists(todo), todo
    assert os.path.exists(ready), ready

    todos = []
    for item in os.listdir(todo):
        current = os.path.join(todo, item, link.JOB_FILE_NAME)
        if not os.path.exists(current):
            utila.error('Job does not exists: %s' % current)
            continue
        todos.append(link.job_load(current))

    readys = []
    for item in os.listdir(ready):
        current = os.path.join(ready, item, link.JOB_FILE_NAME)
        if not os.path.exists(current):
            utila.error('Job does not exists: %s' % current)
            continue
        readys.append(link.job_load(current))

    return todos, readys


def free_todo():
    """Generate file name which does not exists"""
    path = configo.todo()
    name = utila.tmpname()
    while os.path.exists(os.path.join(path, name)):
        name = utila.tmpname()
    return name


def create_todo(file, filename):
    """Create working folder, add info.yaml and write `file` to todo dir"""
    name = free_todo()
    todo_path = configo.todo()

    path = os.path.join(todo_path, name)
    assert not os.path.exists(path)

    os.makedirs(path)
    file_path = os.path.join(path, name)
    info_path = os.path.join(path, link.JOB_FILE_NAME)
    # Copy provied file to todo location
    file.save(file_path)

    # filename = secure_filename(file.filename)
    # Create job information
    job = link.JobInfo(title=filename, date=utila.today(), index=name)
    link.job_dump(info_path, job)

    return path
