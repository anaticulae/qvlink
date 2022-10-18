# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import link


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
    utila.log(f'load debug from: {path}')
    content = utila.from_raw_or_path(path, ftype='', fname='debug')
    result = {}
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line[0] == '#':
            continue
        try:
            separator = '==' if '==' in line else ' '
            package, version = line.split(separator)
        except ValueError:
            continue
        result[package] = version
    return result


RUNNABLE = utila.splitlines("""
queuemo
rawmaker
""")


def write_debug(
    document: str,
    todo: list = None,
    expect: bool = None,
    sort: bool = True,
    requirements: bool = False,
):
    """Write versions of used programs `todo` to ready folder as debug file.

    Args:
        document(str): document id
        todo(list): list of used programs
        expect(bool): Use None to avoid failing when one of `todo` fails
        sort(bool): run `todo` in sorted order
        requirements(bool): write debug as pip compatible style
    """
    ready = link.ready(document)
    if todo is None:
        todo = RUNNABLE
    if sort:
        todo = sorted(todo)
    debug = os.path.join(ready, 'debug')
    with utila.GeorgFork(process=False, returncode=False) as fork:
        for program in todo:
            fork.fork(utila.run, cmd=f'{program} -v -V', expect=expect)
    raw = utila.NEWLINE.join([item.stdout.strip() for item in fork.result])
    if requirements:
        raw = raw.replace(' ', '==')
    utila.log(f'write debug: {debug}')
    utila.file_replace(debug, raw)


def publish_statistics(document: str, debug: bool = True):
    if not debug:
        utila.debug('skip publish statistics')
        return
    ready = link.ready(document)
    cmd = f'qcon -i {ready} --publish'
    completed = utila.run(
        cmd,
        expect=None,
    )
    if completed.returncode:
        utila.error('could not publish `qcon`')
        utila.error(completed)
