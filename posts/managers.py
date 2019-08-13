from django.db import models
from django.db.models import Q


class PostQuerySet(models.QuerySet):
    def search_content(self, query):
        lookups = Q(content__icontains=query)
        return self.filter(lookups).distinct()


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self.db)

    def search_content(self, query):
        return self.get_queryset().search_content(query)

