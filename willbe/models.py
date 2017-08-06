# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class BaseModel(models.Model):
    created_by = models.CharField(max_length=32)
    updated_by = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
