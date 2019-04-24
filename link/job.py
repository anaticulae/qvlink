# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""A user uploads a document. While this process, the pdf document is uploaded
and a folder in `common-todo` is created. This folder contains a JobInfo
info.yaml with with a short work status. This info is shared, and also used
for the finished jobs. """
from dataclasses import dataclass
from os import listdir
from os.path import exists
from os.path import join

from utila import file_create
from utila import file_read
from utila import logging_error
from yaml import SafeLoader
from yaml import dump as yaml_dump
from yaml import load as yaml_load

FILE_NAME = 'info.yaml'


@dataclass
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
    dumped = yaml_dump(result)
    file_create(path, dumped)


def load(path: str) -> JobInfo:
    """Load `JobInfo` from given `path`"""
    assert exists(path), path

    loaded = file_read(path)
    config = yaml_load(loaded, SafeLoader)

    result = JobInfo(
        title=config['title'],
        date=config['date'],
        result=config['result'],
        index=config['index'],
    )
    return result
