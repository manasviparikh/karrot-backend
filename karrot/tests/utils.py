from contextlib import contextmanager

from django.apps import apps
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase
from huey.signals import SIGNAL_SCHEDULED
from huey.contrib.djhuey import signal, disconnect_signal


# Mostly based on this nice persons article:
#   https://www.caktusgroup.com/blog/2016/02/02/writing-unit-tests-django-migrations/
class TestMigrations(TestCase):
    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    migrate_from = None
    migrate_to = None

    def setUp(self):
        assert self.migrate_from and self.migrate_to, \
            "TestCase '{}' must define migrate_from and migrate_to properties".format(type(self).__name__)

        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to the original migration
        executor.migrate(self.migrate_from)

        self.setUpBeforeMigration(old_apps)

        # Run the migration to test
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()  # reload.
        executor.migrate(self.migrate_to)

        self.apps = executor.loader.project_state(self.migrate_to).apps

    def setUpBeforeMigration(self, apps):
        pass


class ExtractPaginationMixin(object):
    def get_results(self, *args, **kwargs):
        """Overrides response.data to remove the pagination control in tests"""
        response = self.client.get(*args, **kwargs)
        if 'results' in response.data:
            response.data = response.data['results']
        return response


@contextmanager
def execute_scheduled_tasks_immediately():
    @signal(SIGNAL_SCHEDULED)
    def task_scheduled_handler(signal, task, exc=None):
        task.execute()

    yield

    disconnect_signal(task_scheduled_handler)
