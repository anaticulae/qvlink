# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila

import link

ONE_HOUR = configo.HV_INT_PLUS(default=60 * 60)


def remove_outdated():
    outdated = determine_outdated()
    for documentid in outdated:
        utila.log(f'complete/fail: {documentid}')
        error = 'not completed in given time'
        link.fail(documentid, error=error)


def determine_outdated():
    todopath = configo.todo(True)
    result = []
    for documentid in os.listdir(todopath):
        info = os.path.join(todopath, documentid, link.JOBFILE_NAME)
        if not utila.exists(info):
            utila.error(f'file does not exists: {info}')
            result.append(documentid)
            continue
        if utila.file_age(info) < ONE_HOUR.value:
            continue
        if link.failed(documentid):
            # already failed
            continue
        if link.current(documentid) == link.ProcessState.PUBLISHED:
            continue
        if link.current(documentid) == link.ProcessState.ERROR:
            continue
        result.append(documentid)
    return result
