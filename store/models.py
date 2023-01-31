from django.db import models

from users.models import User


class Store(models.Model):
    store_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    store_name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=15)
    latitude = models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True)
    longitude = models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True)
    is_waiting = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    information = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'store'

