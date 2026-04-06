import os
import sys
import importlib
from typing import Optional  # NOQA
from django.apps import apps

_jobs = None


def noneimplementation(meth):
    pass


class JobError(Exception):
    pass


class BaseJob:
    help = "undefined job description."
    when = None  # type: Optional[str]

    def execute(self):
        raise NotImplementedError("Job needs to implement the execute method")


class MinutelyJob(BaseJob):
    when = "minutely"


class QuarterHourlyJob(BaseJob):
    when = "quarter_hourly"


class HourlyJob(BaseJob):
    when = "hourly"


class DailyJob(BaseJob):
    when = "daily"


class WeeklyJob(BaseJob):
    when = "weekly"


class MonthlyJob(BaseJob):
    when = "monthly"


class YearlyJob(BaseJob):
    when = "yearly"


def my_import(name):
    pass


def find_jobs(jobs_dir):
    pass


def find_job_module(app_name: str, when: Optional[str] = None) -> str:
    """Find the directory path to a job module."""
    pass


def import_job(app_name, name, when=None):
    pass


def get_jobs(when=None, only_scheduled=False):
    """
    Return a dictionary mapping of job names together with their respective
    application class.
    """
    pass


def get_job(app_name, job_name):
    pass


def print_jobs(
    when=None,
    only_scheduled=False,
    show_when=True,
    show_appname=False,
    show_header=True,
):
    pass
