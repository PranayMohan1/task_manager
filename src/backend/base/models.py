from django.db import models
from django.utils.translation import ugettext_lazy as ul


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(ul('created'), auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(ul('modified'), auto_now=True)

    class Meta:
        abstract = True