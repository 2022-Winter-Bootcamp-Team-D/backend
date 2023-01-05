from django.db import models
from enum import Enum


class Store(models.Model):
    store_id = models.BigAutoField(primary_key=True)
    store_name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    is_waiting = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    information = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'store'

