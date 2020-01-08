# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""A user uploads a document. While this process, the pdf document is uploaded
and a folder in `common-todo` is created.

This folder contains a JobInfo info.yaml with with a short work status.
This info is shared, and also used for the finished jobs.
"""
import dataclasses
import os

import configo
import utila
import yaml

FILE_NAME = 'info.yaml'


@dataclasses.dataclass
class JobInfo:
    """Short description for identifying the job"""
    title: str
    date: str
    index: int
    result: str = None


def dump(path: str, info: JobInfo):
    """Save `info` to given `path`"""
    result = {
        'title': info.title,
        'date': info.date,
        'result': info.result,
        'index': info.index,
    }
    dumped = yaml.dump(result)
    utila.file_create(path, dumped)


def load(path: str) -> JobInfo:
    """Load `JobInfo` from given `path`"""
    assert os.path.exists(path), path

    loaded = utila.file_read(path)
    config = yaml.load(loaded, yaml.SafeLoader)

    result = JobInfo(
        title=config['title'],
        date=config['date'],
        result=config['result'],
        index=config['index'],
    )
    return result


def todo_count() -> int:
    """Count folder in common `todo` folder

    Returns:
        count of valid todo folder in todo path
    """
    path = configo.todo()
    dirs = [
        item for item in os.listdir(path)
        if valid_todo(os.path.join(path, item))
    ]
    return len(dirs)


def ready_count() -> int:
    """Count folder in common `ready` folder

    Returns:
        count of valid ready folder in ready path
    """
    path = configo.ready()
    dirs = [
        item for item in os.listdir(path)
        if valid_ready(os.path.join(path, item))
    ]
    return len(dirs)


def valid_todo(path: str) -> bool:
    """Check that `path` is a valid todo folder with required files

    Args:
        path(str): path to possible todo folder
    Returns:
        True if folder is a valid todo folder else False
    """
    if not os.path.isdir(path):
        return False
    if not os.path.exists(os.path.join(path, FILE_NAME)):
        return False
    return True


def valid_ready(path: str):
    #TODO: Special check for ready is required. E.g. result in percent
    return valid_todo(path)
