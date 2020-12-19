#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import link.__patch__
# control
from link.control import delete
from link.control import finish_fastview
from link.control import finish_resultview
from link.control import publish
from link.control import start_analysis
from link.control import start_progress
from link.control import verify
from link.control import write_optimized_findings
# Job
from link.job import JOB_FILE_NAME
from link.job import NO_FINDINGS
from link.job import PUBLIC_OWNER
from link.job import FindingStatus
from link.job import JobInfo
from link.job import count_ready
from link.job import count_todo
from link.job import dump_job
from link.job import load_job
# state
from link.state import ProcessState
from link.state import current
from link.state import document
from link.state import done_ as done
from link.state import fastview
from link.state import fastview_done
from link.state import inprogress
from link.state import load_jobinfo
from link.state import optimized
from link.state import owner
from link.state import pdfinfo
from link.state import ready
from link.state import ready_deleted
from link.state import resultview
from link.state import resultview_done
from link.state import todo
from link.state import todo_deleted
# Workspace
from link.workspace import collect_jobs
from link.workspace import create_todo
from link.workspace import find_free_todo
from link.workspace import sortable_date

__version__ = '2.0.4'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# use 16 chars/ints to create random job name
DOCUMENT_ID_LENGTH = 16
