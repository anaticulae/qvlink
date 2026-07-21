# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
import resinf
import utilo

import qvlink
from tests.fixtures import broken  # pylint:disable=W0611
from tests.fixtures import common  # pylint:disable=W0611
from tests.fixtures import completed  # pylint:disable=W0611
from tests.fixtures import example  # pylint:disable=W0611
from tests.fixtures import withfindings  # pylint:disable=W0611

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

if 'SHARED_READY' not in os.environ:
    utilo.debug('SET SHARED_READY')
    DIR = utilo.tmpdir(qvlink.ROOT)
    configos.export(
        utilo.join(DIR, 'common'),
        utilo.join(DIR, 'todo'),
        utilo.join(DIR, 'ready'),
    )

resinf.setup(qvlink.ROOT)
