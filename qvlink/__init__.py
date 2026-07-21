#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import importlib.metadata
import os

import qvlink.__patch__
# cleaner
from qvlink.cleaner import remove_outdated
# control
from qvlink.control import PROGRESS_START
from qvlink.control import delete
from qvlink.control import finish_fastview
from qvlink.control import finish_resultview
from qvlink.control import publish
from qvlink.control import start_analysis
from qvlink.control import start_progress
from qvlink.control import verify
from qvlink.control import write_optimized_findings
# debug
from qvlink.debug import load_debug
from qvlink.debug import publish_statistics
from qvlink.debug import write_debug
# Job
from qvlink.job import JOBFILE_NAME
from qvlink.job import NO_FINDINGS
from qvlink.job import PUBLIC_OWNER
from qvlink.job import FindingStatus
from qvlink.job import JobInfo
from qvlink.job import JobInfos
from qvlink.job import count_ready
from qvlink.job import count_todo
from qvlink.job import dump_job
from qvlink.job import job_title
from qvlink.job import load_job
from qvlink.job import save_job
# state
from qvlink.state import ProcessState
from qvlink.state import State
from qvlink.state import current
from qvlink.state import deleted
from qvlink.state import document
from qvlink.state import done_ as done
from qvlink.state import fail
from qvlink.state import failed
from qvlink.state import fastview
from qvlink.state import fastview_done
from qvlink.state import inprogress
from qvlink.state import inprogressed
from qvlink.state import load_jobinfo
from qvlink.state import load_jobinfo_raw
from qvlink.state import nosupport
from qvlink.state import notsupported
from qvlink.state import optimized
from qvlink.state import owner
from qvlink.state import pdfinfo
from qvlink.state import pdfinfo_path
from qvlink.state import private
from qvlink.state import progress
from qvlink.state import ready
from qvlink.state import ready_deleted
from qvlink.state import resultview
from qvlink.state import resultview_done
from qvlink.state import todo
from qvlink.state import todo_deleted
from qvlink.state import update_bookkeeping
from qvlink.state import update_progress
from qvlink.state import update_progress_step
# Workspace
from qvlink.workspace import collect_jobs
from qvlink.workspace import create_todo
from qvlink.workspace import find_free_todo
from qvlink.workspace import load_documents
from qvlink.workspace import sortable_date

__version__ = importlib.metadata.version('qvlink')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# use 16 chars/ints to create random job name
DOCUMENT_ID_LENGTH = 16

PDFINFO_NAME = 'pdflog.yaml'
JOB_FILE_NAME = JOBFILE_NAME  # TODO: REMOVE LATER
