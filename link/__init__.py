#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import os

# Job
from link.job import FILE_NAME as JOB_FILE_NAME
from link.job import JobInfo
from link.job import dump as job_dump
from link.job import load as job_load
from link.job import ready_count
from link.job import todo_count
# Workspace
from link.workspace import create_todo
from link.workspace import current_date
from link.workspace import free_todo
from link.workspace import scan
from link.workspace import sortable_date

__version__ = '0.2.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
