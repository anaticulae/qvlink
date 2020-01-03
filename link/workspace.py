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


def free_todo(todopath: str = None) -> str:
    """Generate file name which does not exists.

    Args:
        todopath(str): Path to location where todos are written. If None
                   the todopath of `configo.todo()` is used.
    Returns:
        Name of process number/folder name which is not used yet.
    Hint:
        This method is not thread safe.
    """
    if todopath is None:
        todopath = configo.todo()
    name = utila.tmpname()
    while os.path.exists(os.path.join(todopath, name)):
        name = utila.tmpname()
    return name


def create_todo(file, filename, todopath: str = None) -> str:
    """Create working folder, add info.yaml and write `file` to todo dir

    Args:
        file(str): path to source file
        filename(str): name of saved pdf file - not very important
        todopath(str): Path to location where todos are written. If None
                       the todopath of `configo.todo()` is used.
    Returns:
        path to created todo with job content
    """
    name = free_todo(todopath)
    if todopath is None:
        todopath = configo.todo()

    path = os.path.join(todopath, name)
    assert not os.path.exists(path)

    os.makedirs(path)
    file_path = os.path.join(path, name)
    info_path = os.path.join(path, link.JOB_FILE_NAME)
    # Copy provied file to todo location
    file.save(file_path)

    # filename = secure_filename(file.filename)
    # Create job information
    date = current_date()
    job = link.JobInfo(title=filename, date=date, index=name)
    link.job_dump(info_path, job)
    return path


def current_date() -> str:
    """Determine current date and time

    Format:
        year:month:day hour:second
    """
    return f'{utila.today()} {utila.current()}'


def sortable_date(date: str) -> str:
    """Make date sortable due transform to alphabetical, sortable string.

    Args:
        date(str): year:month:day hour:second
    Returns:
        sortable str representation
    """
    # Sort by year, month, day, hour, second
    date = date[6:10] + date[3:5] + date[0:2] + date[11:13] + date[14:16]
    assert len(date) == 12, date
    return date
