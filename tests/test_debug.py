# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import qvlink


def test_debug_write_and_load(testdir, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(qvlink, 'ready', lambda x: x)
        qvlink.write_debug(testdir.tmpdir, todo=['rawmaker'])
    debug = qvlink.load_debug('debug')
    assert debug['rawmaker']


def test_debug_write_requirements(testdir, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(qvlink, 'ready', lambda x: x)
        qvlink.write_debug(
            testdir.tmpdir,
            todo=['rawmaker'],
            requirements=True,
        )
    debug = qvlink.load_debug('debug')
    assert debug['rawmaker']
