from django.db import models


class Query(models.Model):
    text = models.TextField(primary_key=True)
    popular_words = models.TextField(null=False)
    num_results = models.BigIntegerField(null=False)
    client_ip = models.TextField()

    def get_absolute_url(self):
        return f"/search/{self.text}"


class Link(models.Model):
    qu = models.ForeignKey(to=Query, on_delete=models.CASCADE)
    title = models.TextField()
    link = models.URLField()
    description = models.TextField()
    position = models.PositiveIntegerField()
