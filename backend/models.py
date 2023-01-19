from django.db import models

from waiting.models import Waiting


class Token(models.Model):
    # token_id = models.BigAutoField()
    token = models.CharField(max_length=200)
    waiting_id = models.ForeignKey(Waiting, primary_key=True, on_delete=models.CASCADE, db_column='token_id')

    class Meta:
        db_table = 'token'
