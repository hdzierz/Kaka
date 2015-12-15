from django.apps import AppConfig
from .sync import sync_with_genotype_db as synchronise


class ExperimentSearchConfig(AppConfig):

    name = 'experimentsearch'
    verbose_name = 'Experiment Search'

    has_run = False

    def ready(self):
        if not self.has_run:
            synchronise()
            self.has_run = True
