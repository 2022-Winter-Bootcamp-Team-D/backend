from django.db import models
from enum import Enum


class Store(models.Model):
    storeId = models.BigAutoField(primary_key=True)
    store_name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=50, unique=True)
    is_waiting = models.BooleanField()
    is_delete = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    information = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'store'

