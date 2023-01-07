from django.db import models
from store.models import Store


class Waiting(models.Model):
    class Status(models.TextChoices):
        WAITING = 'WA'
        CANCELED = 'CN'
        ENTERED = 'EN'

    waiting_id = models.BigAutoField(primary_key=True)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    phone_num = models.CharField(max_length=20)
    people = models.SmallIntegerField()
    password = models.CharField(max_length=4)
    status = models.CharField(max_length=2, default='WA', choices=Status.choices)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'waiting'
