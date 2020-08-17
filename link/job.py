# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Job
===

Describes current working status of one document which was uploaded by a user.

1. While uploading a pdf file, a job folder in `common-todo` is created.
2. This folder contains a JobInfo info.yaml with a short work status.
3. This info is shared and also used for the finished job.
"""

import collections
import dataclasses
import os

import configo
import utila
import yaml

JOB_FILE_NAME = 'info.yaml'

FindingStatus = collections.namedtuple('FindingStatus', 'open closed excluded')


@dataclasses.dataclass
class JobInfo:
    """Short description for identifying the job."""
    title: str
    date: str
    index: int
    result: FindingStatus = None
    done: bool = False
    password: str = None
    hashlink: str = None


def dump_job(path: str, info: JobInfo):
    """Save `info` to given `path`."""
    result = {
        'title': info.title,
        'date': info.date,
        'result': findingstatus_toraw(info.result),
        'index': info.index,
        'done': info.done,
    }
    if info.password:
        result['password'] = info.password
    if info.hashlink:
        result['hashlink'] = info.hashlink

    dumped = yaml.dump(result)
    utila.file_create(path, dumped)


def findingstatus_toraw(item: FindingStatus) -> dict:
    try:
        return {
            'open': item.open,
            'closed': item.closed,
            'excluded': item.excluded
        }
    except (AttributeError, TypeError):
        return None


def findingstatus_fromdict(items: dict, default=None) -> FindingStatus:
    # TODO: REPLACE WITH A SMART ALTERNATIVE
    try:
        result = FindingStatus(
            items['open'],
            items['closed'],
            items['excluded'],
        )
    except (AttributeError, TypeError):
        return default
    return result


def load_job(path: str) -> JobInfo:
    """Load `JobInfo` from given `path`"""
    assert os.path.exists(path), path

    loaded = utila.file_read(path)
    config = yaml.load(loaded, yaml.SafeLoader)

    findings = config.get('result', None)
    loaded = findingstatus_fromdict(findings)
    if loaded:
        findings = loaded
    else:
        # TODO: REMOVE AFTER CHANGING FROM INT TO FINDINGSTATUS COMPLETED
        if findings:
            findings = None
        else:
            findings = FindingStatus(0, 0, 0)

    result = JobInfo(
        title=config['title'],
        date=config['date'],
        result=findings,
        index=config['index'],
        done=config.get('done', False),
        password=config.get('password', None),
        hashlink=config.get('hashlink', None),
    )
    return result


def count_todo() -> int:
    """Count folder in common `todo` folder.

    Returns:
        count of valid todo folder in todo path
    """
    path = configo.todo()
    dirs = [
        item for item in os.listdir(path)
        if validate_todo(os.path.join(path, item))
    ]
    return len(dirs)


def count_ready() -> int:
    """Count folder in common `ready` folder.

    Returns:
        count of valid ready folder in ready path
    """
    path = configo.ready()
    dirs = [
        item for item in os.listdir(path)
        if validate_ready(os.path.join(path, item))
    ]
    return len(dirs)


def validate_todo(path: str) -> bool:
    """Check that `path` is a valid todo folder with required files.

    Args:
        path(str): path to possible todo folder
    Returns:
        True if folder is a valid todo folder else False
    """
    if not os.path.isdir(path):
        return False
    if not os.path.exists(os.path.join(path, JOB_FILE_NAME)):
        return False
    return True


def validate_ready(path: str):
    #TODO: Special check for ready is required. E.g. result in percent
    return validate_todo(path)
