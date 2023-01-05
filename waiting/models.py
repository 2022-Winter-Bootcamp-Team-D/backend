from django.db import models
from store.models import Store


class Waiting(models.Model):
    Status = [
        ('CN', 'CANCELED'),
        ('WA', 'WAITING'),
        ('EN', 'ENTERED'),
        ]

    waiting_id = models.BigAutoField(primary_key=True)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    phone_num = models.CharField(max_length=20)
    people = models.SmallIntegerField()
    password = models.SmallIntegerField()
    status = models.BooleanField(default='WA', choices=Status)
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'waiting'
