from django.db import models
from clairview.models import Experiment


class WebExperimentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type="web")


class WebExperiment(Experiment):
    objects = WebExperimentManager()  # type: ignore

    class Meta:
        proxy = True