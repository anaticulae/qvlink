#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import link.__patch__
# cleaner
from link.cleaner import remove_outdated
# control
from link.control import PROGRESS_START
from link.control import delete
from link.control import finish_fastview
from link.control import finish_resultview
from link.control import publish
from link.control import start_analysis
from link.control import start_progress
from link.control import verify
from link.control import write_optimized_findings
# debug
from link.debug import load_debug
from link.debug import publish_statistics
from link.debug import write_debug
# Job
from link.job import JOBFILE_NAME
from link.job import NO_FINDINGS
from link.job import PUBLIC_OWNER
from link.job import FindingStatus
from link.job import JobInfo
from link.job import JobInfos
from link.job import count_ready
from link.job import count_todo
from link.job import dump_job
from link.job import job_title
from link.job import load_job
from link.job import save_job
# state
from link.state import ProcessState
from link.state import State
from link.state import current
from link.state import deleted
from link.state import document
from link.state import done_ as done
from link.state import fail
from link.state import failed
from link.state import fastview
from link.state import fastview_done
from link.state import inprogress
from link.state import inprogressed
from link.state import load_jobinfo
from link.state import load_jobinfo_raw
from link.state import nosupport
from link.state import notsupported
from link.state import optimized
from link.state import owner
from link.state import pdfinfo
from link.state import pdfinfo_path
from link.state import private
from link.state import progress
from link.state import ready
from link.state import ready_deleted
from link.state import resultview
from link.state import resultview_done
from link.state import todo
from link.state import todo_deleted
from link.state import update_bookkeeping
from link.state import update_progress
from link.state import update_progress_step
# Workspace
from link.workspace import collect_jobs
from link.workspace import create_todo
from link.workspace import find_free_todo
from link.workspace import load_documents
from link.workspace import sortable_date

__version__ = '2.15.3'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# use 16 chars/ints to create random job name
DOCUMENT_ID_LENGTH = 16

PDFINFO_NAME = 'pdfinfo.yaml'
JOB_FILE_NAME = JOBFILE_NAME  # TODO: REMOVE LATER
