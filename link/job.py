# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

import link

JOB_FILE_NAME = 'info.yaml'

FindingStatus = collections.namedtuple('FindingStatus', 'open closed excluded')

PUBLIC_OWNER = '00000000'


@dataclasses.dataclass
class JobInfo:
    """Short description for identifying the job."""
    title: str
    date: str
    name: str
    result: FindingStatus = None
    # TODO: REPLACE DONE BY PROPERTY DONE WITH STATE CHECK
    done: bool = False
    password: str = None
    hashlink: str = None
    owner: str = None
    state: int = None

    def __post_init__(self):
        assert isinstance(self.name, str), type(self.name)


def dump_job(info: JobInfo, convert: bool = True) -> str:
    """Convert to yaml representation."""
    result = {
        'title': info.title,
        'date': info.date,
        'result': findingstatus_toraw(info.result),
        'name': info.name,
        'done': info.done,
        'owner': info.owner,
        'state': info.state,
    }
    if info.password:
        result['password'] = info.password
    if info.hashlink:
        result['hashlink'] = info.hashlink
    # convert to yaml
    dumped = yaml.dump(result) if convert else result
    return dumped


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


NO_FINDINGS = FindingStatus(0, 0, 0)


def load_job(path: str) -> JobInfo:
    """Load `JobInfo` from given `path` or yaml raw str."""
    config = utila.yaml_from_raw_or_path(
        path,
        fname='info',
    )

    findings = findingstatus_fromdict(
        config.get('result', None),
        default=NO_FINDINGS,
    )

    result = JobInfo(
        title=config['title'],
        date=config['date'],
        result=findings,
        name=config['name'],
        owner=config['owner'],
        done=config.get('done', False),
        state=config.get('state', None),
        password=config.get('password', None),
        hashlink=config.get('hashlink', None),
    )
    return result


def save_job(info: JobInfo, done: bool = True):
    documentid = info.name
    outpath = link.ready(documentid) if done else link.todo(documentid)
    outpath = os.path.join(outpath, JOB_FILE_NAME)
    utila.debug(f'update jobinfo: {outpath}')
    dumped = dump_job(info)
    utila.file_replace(outpath, dumped)


def load_debug(path: str) -> dict:
    """Debug information of software which was used to create this run.

    The number of queuemo defines all other dependencies, but it is
    possible to store more data.

    Args:
        path(str): path/content to/of debug file or folder which
                   contains the file
    Returns:
        dict with package -> version
    """
    content = utila.from_raw_or_path(path, ftype='', fname='debug')
    result = {}
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line[0] == '#':
            continue
        try:
            package, version = line.split()
        except ValueError:
            continue
        result[package] = version
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
