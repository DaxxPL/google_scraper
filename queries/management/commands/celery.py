import sys

import shlex
import subprocess
from django.core.management.base import BaseCommand
from django.utils import autoreload


class Command(BaseCommand):
    def handle(self, *args, **options):
        autoreload.run_with_reloader(self._restart_celery)

    @classmethod
    def _restart_celery(cls):
        cls.run('pkill celery')
        cls.run('celery worker -l info -A google_scraper')

    @staticmethod
    def run(cmd):
        subprocess.call(shlex.split(cmd))