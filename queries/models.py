from django.db import models
import re
from collections import Counter
from .selenium_data import give_results


class Query(models.Model):
    text = models.TextField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    popular_words = models.TextField(null=False)
    num_results = models.PositiveIntegerField(null=False)
    client_ip = models.TextField()

    @staticmethod
    def count_words(links):
        my_list = [link.description.strip()+' '+link.title.strip() for link in links]
        my_list = [re.sub(r'[^\w\s]', '', s) for s in my_list]
        my_list = [re.sub(r'\W*\b\w{1,2}\b', '', s) for s in my_list]
        my_list = [re.sub(r'[0-9]+', '', s) for s in my_list]
        count = Counter(word.lower() for line in my_list
                        for word in line.split())
        return [i[0] for i in count.most_common(10)]

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        results = give_results(self.text)
        self.num_results = results[0]
        insert_list = []
        for item in results[1:]:
            insert_list.append(Link(qu=self, title=item['title'], link=item['link'], description=item['text'],
                                    position=item['rank'],))
        self.popular_words = Query.count_words(insert_list)
        super().save(force_insert, force_update, using, update_fields)
        Link.objects.bulk_create(insert_list)

    def get_absolute_url(self):
        return f"/search/{self.text}"


class Link(models.Model):
    qu = models.ForeignKey(to=Query, on_delete=models.CASCADE)
    title = models.TextField()
    link = models.URLField()
    description = models.TextField()
    position = models.PositiveIntegerField()


