# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import link
import tests.patch


def test_optimize_findings(common, monkeypatch):
    with tests.patch.patch_todo(common, monkeypatch):
        link.write_optimized_findings(document='5555')
