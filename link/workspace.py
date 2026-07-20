# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
import utilo

import link


def collect_jobs(
    path: str = None,
    owner: str = None,
    *,
    skip_removed: bool = False,
) -> tuple:
    """Scan common space for jobs todo and done.

    Args:
        path(str): path to temporary directory
        skip_removed(bool): skip jobs which contain deleted mark
        owner(str): skip all jobs which does not match owner id. Options:
               - None: do not check owner id
               - PUBLIC: 00000000
               - Rest
    Returns:
        tuple of collected (todos, readys)
    """
    if path is None:
        todo = configos.todo()
        ready = configos.ready()
    else:
        assert os.path.exists(path), path
        todo = os.path.join(path, 'todo')
        ready = os.path.join(path, 'ready')
    # ensure that todo and ready exists
    assert os.path.exists(todo), todo
    assert os.path.exists(ready), ready
    # collect jobs depending on state
    todos = collect_job_folder(todo, skip_removed=skip_removed)
    readys = collect_job_folder(ready, skip_removed=skip_removed)
    # filter jobs by owner
    if owner:
        # support multiple owner, eg. public, owner
        owner = {owner} if isinstance(owner, str) else owner
        todos = [item for item in todos if item.owner in owner]
        readys = [item for item in readys if item.owner in owner]
    return todos, readys


def collect_job_folder(
    folder: str,
    skip_removed: bool = False,
):
    result = []
    for item in os.listdir(folder):
        current = os.path.join(folder, item, link.JOBFILE_NAME)
        if not os.path.exists(current):
            utilo.error(f'job does not exists: {current}')
            continue
        if skip_removed:
            # TODO: REPLACE LATER
            removed = os.path.join(folder, item, 'deleted')
            if os.path.exists(removed):
                utilo.info(f'skip removed: {removed}')
                continue
        result.append(link.load_job(current))
    return result


def find_free_todo(todopath: str = None) -> str:
    """Generate file name which does not exists.

    Args:
        todopath(str): Path to location where todos are written. If None
                   the todopath of `configos.todo()` is used.
    Returns:
        Name of process number/folder name which is not used yet.
    Hint:
        This method is not thread safe.
    """
    if todopath is None:
        todopath = configos.todo()
    name = utilo.tmpname(width=link.DOCUMENT_ID_LENGTH)
    while os.path.exists(os.path.join(todopath, name)):  # pylint:disable=W0149
        name = utilo.tmpname(width=link.DOCUMENT_ID_LENGTH)
    return name


def create_todo(
    file,
    filename: str = 'default.pdf',
    todopath: str = None,
    todoname: str = None,
    owner: str = None,
    *,
    exist_ok: bool = False,
) -> str:
    """Create working folder, add jobinfo.yaml and write `file` to todo dir

    Args:
        file(str): path to source file
        filename(str): name of saved pdf file - not very important
        todopath(str): path to location where todos are written. If None
                       the todopath of `configos.todo()` is used.
        todoname(str): name of todo folder to save file in. If None
                       todoname is automatically generated.
        owner(str): user which can access document
        exist_ok(bool): do not fail on existing output directory
    Returns:
        path to created todo with job content
    """
    if todoname is None:
        todoname = find_free_todo(todopath)
    if todopath is None:
        todopath = configos.todo()
    path = os.path.join(todopath, todoname)
    os.makedirs(path, exist_ok=exist_ok)
    filepath = os.path.join(path, todoname)
    infopath = os.path.join(path, link.JOBFILE_NAME)
    # Copy provied file to todo location
    try:
        file.save(filepath)
    except AttributeError:
        # Support path to file as input
        utilo.file_copy(file, filepath)
    # filename = secure_filename(file.filename)
    # Create job information
    date = utilo.timedate()
    job = link.JobInfo(title=filename, date=date, name=todoname, owner=owner)
    dumped = link.dump_job(job)
    utilo.file_create(infopath, dumped)
    return path


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


def load_documents(common, owner: str, state: link.State = None) -> list:
    todo, ready = link.collect_jobs(
        common,
        skip_removed=True,
        owner=owner,
    )
    dones = {item.name for item in ready}
    if state in (link.State.RUNNING, link.State.WAITING):
        ready.clear()
    result = [link.load_jobinfo_raw(item.name, done=None) for item in ready]
    for item in result:
        item['done'] = True
    if state == link.State.DONE:
        # do not load jobs which are not done
        todo.clear()
    for item in todo:
        if item.name in dones:
            continue
        current = link.load_jobinfo_raw(item.name, done=None)
        if state is not None:
            item_state = link.State(current['state'])
            if item_state != state:
                continue
        result.append(current)
    result = sorted(
        result,
        key=lambda item: item['date'],
        reverse=True,
    )
    return result
