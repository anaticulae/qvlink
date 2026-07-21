# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Job
===

Describes current working status of one document which was uploaded by a user.

1. While uploading a pdf file, a job folder in `common-todo` is created.
2. This folder contains a JobInfo jobinfo.yaml with a short work status.
3. This info is shared and also used for the finished job.
"""

import collections
import dataclasses
import json
import os

import configos
import utilo

import qvlink

JOBFILE_NAME = 'jobinfo.yaml'

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

    @property
    def documentid(self) -> str:
        return self.name

    def __post_init__(self):
        assert isinstance(self.name, str), type(self.name)


JobInfos = 'list[JobInfo]'  # pylint:disable=C0103


def dump_job(
    info: JobInfo,
    convert: str = 'yaml',
    password: bool = True,
) -> str:
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
        result['password'] = info.password if password else 'XXXXXXXXXXXXXXX'
    if info.hashlink:
        result['hashlink'] = info.hashlink
    dumped = result
    if convert == 'yaml':
        dumped: str = utilo.yaml_dump(dumped)
    if convert == 'json':
        dumped: str = json.dumps(dumped)
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
    config = utilo.yaml_from_raw_or_path(
        path,
        fname=utilo.file_name(JOBFILE_NAME),
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
    outpath = qvlink.ready(documentid) if done else qvlink.todo(documentid)
    outpath = os.path.join(outpath, JOBFILE_NAME)
    utilo.debug(f'save jobinfo: {outpath} {done}')
    dumped = dump_job(info)
    utilo.file_replace(outpath, dumped)


def count_todo() -> int:
    """Count folder in common `todo` folder.

    Returns:
        count of valid todo folder in todo path
    """
    path = configos.todo()
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
    path = configos.ready()
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
    if not os.path.exists(os.path.join(path, JOBFILE_NAME)):
        return False
    return True


def validate_ready(path: str):
    #TODO: Special check for ready is required. E.g. result in percent
    return validate_todo(path)


def job_title(documentid: str) -> str:
    done = utilo.exists(qvlink.done(documentid))
    info = qvlink.load_jobinfo(
        documentid=documentid,
        done=done,
    )
    title = info.title
    title = title.rstrip('.pdf')
    return title
