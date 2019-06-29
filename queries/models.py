from django.db import models


class Query(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
