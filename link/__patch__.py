# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import glob
import os
import shutil

import utila
import utila.file


def copy_content(  # pylint:disable=R1260
        source: str,
        destination: str,
        pattern: str = None,
        *,
        recursive: bool = False,
        update: bool = False,
        skip_equal: bool = False,
        verbose: bool = False,
):
    """Copy the content from `source` to `destination` folder. If
    `destination` folder does not exists, it will be created.

    Args:
        source(str): file or directory to copy
        destination(str): directory to copy source item(s)
        pattern(str): accept files which matches this pattern, if None
                      all files matches.

        recursive(bool): if True, copy child folder
        update(bool): move only when the source file is newer than the
                      destination file or when the destination file is
                      missing.
        skip_equal(bool): if True, do not raise Error if source and
                          destination is equal.
        verbose(bool): explain what is being done

    Pattern-Syntax:
        In the current implementation only one multiple field is
        possible. The multiple pattern group is inside brackets and is
        separated by |. For example: (rawmaker|groupme)__*.yaml, copies
        rawmaker and groupme yaml files.

    Hint:
        Why not using shutil.copytree?: Copy tree expect that
        destination does not exists, but we need this.
    """
    assert source, str(source)
    assert destination, str(destination)
    suppress = contextlib.suppress if skip_equal else utila.nothing
    if os.path.isfile(source):
        if not utila.isfilepath(destination):
            destination = os.path.join(destination, os.path.basename(source))
        if verbose:
            utila.log(f'cp: {source} -> {destination}')
        with suppress(shutil.SameFileError):
            utila.file_copy(
                source,
                destination,
                update=update,
                exception=skip_equal,
            )
        return

    if pattern is None:
        pattern = '*'

    multiple = utila.file.split_multipattern(pattern)
    if multiple:
        if verbose:
            utila.log(f'split pattern: {pattern} -> {multiple}')
        for converted_pattern in multiple:
            # run multiple operation
            with suppress(shutil.SameFileError):
                copy_content(
                    source,
                    destination,
                    pattern=converted_pattern,
                    recursive=recursive,
                    skip_equal=skip_equal,
                    update=update,
                    verbose=verbose,
                )
        return

    pattern = f'**/{pattern}' if recursive else pattern

    with utila.chdir(source):
        selected = list(glob.glob(pattern, recursive=recursive))

    for item in selected:
        source_ = os.path.join(source, item)
        dest_ = os.path.join(destination, item)
        if os.path.isfile(source_):
            if verbose:
                utila.log(f'cp: {source_} -> {dest_}')
            with suppress(shutil.SameFileError):
                utila.file_copy(
                    source_,
                    dest_,
                    update=update,
                    exception=skip_equal,
                )
        else:
            if verbose:
                utila.log(f'mkdir: {dest_}')
            os.makedirs(dest_, exist_ok=True)


utila.copy_content = copy_content


def file_copy(
        source: str,
        destination: str,
        update: bool = True,
        exception: bool = False,
):
    """Copy a single `source` file to `destination` file or folder.

    Args:
        source(str): path to existing source file
        destination(str): a folder or a file to copy
        update(bool): copy only when the source file is different than
                      the destination file or when the destination file
                      is missing.
        exception(bool): if True  raise exception if copying is not possible
                         if False log error and raise exit
    Raises:
        OSError: if coping is not possible and exception is True
        SameFileError: if source and destination is equal
    """
    assert os.path.exists(source), f'"{source}" does not exists'
    try:
        if update and utila.file_compare(source, destination):
            return
        parent, _ = os.path.split(destination)
        os.makedirs(parent, exist_ok=True)
        shutil.copy(source, destination)
    except OSError as error:
        utila.error(f'could not overwrite: {destination}')
        if exception:
            raise error
        exit(utila.FAILURE)


utila.file_copy = file_copy
