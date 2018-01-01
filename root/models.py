# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class DefaultDecimalField(models.DecimalField):

    def __init__(self):
        max_digits = 32
        decimal_places = 10
        super(DefaultDecimalField, self).__init__(max_digits=max_digits, decimal_places=decimal_places)


class CharField(models.CharField):
    pass


class DatetimeField(models.DateTimeField):
    pass


class CreatedAtField(models.DateTimeField):

    def __init__(self):
        super(CreatedAtField, self).__init__(auto_now_add=True)


class UpdatedAtField(models.DateTimeField):

    def __init__(self):
        super(UpdatedAtField, self).__init__(auto_now=True)


class DefaultForeignKey(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        super(DefaultForeignKey, self).__init__(on_delete=models.CASCADE, *args, **kwargs)


class BaseModel(models.Model):
    created_by = CharField(max_length=32)
    updated_by = CharField(max_length=32)
    created_at = CreatedAtField()
    updated_at = UpdatedAtField()

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True
