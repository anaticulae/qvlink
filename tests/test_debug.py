# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link


def test_debug_write_and_load(testdir, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(link, 'ready', lambda x: x)
        link.write_debug(testdir.tmpdir, todo=['rawmaker'])
    debug = link.load_debug('debug')
    assert debug['rawmaker']


def test_debug_write_requirements(testdir, monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(link, 'ready', lambda x: x)
        link.write_debug(
            testdir.tmpdir,
            todo=['rawmaker'],
            requirements=True,
        )
    debug = link.load_debug('debug')
    assert debug['rawmaker']
