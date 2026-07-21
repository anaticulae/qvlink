# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilotest

import qvlink
import tests.patch


def test_remove_outdated(common, monkeypatch, capsys):
    """Ensure that `broken` is cleaned by remover."""
    with tests.patch.patch_todo(common, monkeypatch):
        qvlink.remove_outdated()
    stderr = utilotest.stdout(capsys)
    # broken is compleated by `remove_outdated`
    assert 'complete/fail: broken' in stderr
