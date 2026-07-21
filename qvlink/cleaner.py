# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
import utilo

import qvlink

ONE_HOUR = configos.HV_INT_PLUS(default=60 * 60)


def remove_outdated():
    outdated = determine_outdated()
    for documentid in outdated:
        utilo.log(f'complete/fail: {documentid}')
        error = 'not completed in given time'
        qvlink.fail(documentid, error=error)


def determine_outdated():
    todopath = configos.todo(True)
    result = []
    for documentid in os.listdir(todopath):
        info = os.path.join(todopath, documentid, qvlink.JOBFILE_NAME)
        if not utilo.exists(info):
            utilo.error(f'file does not exists: {info}')
            result.append(documentid)
            continue
        if utilo.file_age(info) < ONE_HOUR.value:
            continue
        if qvlink.failed(documentid):
            # already failed
            continue
        if qvlink.current(documentid) == qvlink.ProcessState.PUBLISHED:
            continue
        if qvlink.current(documentid) == qvlink.ProcessState.ERROR:
            continue
        result.append(documentid)
    return result
