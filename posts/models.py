from django.conf import settings
from django.db import models
from django.urls import reverse
from .managers import PostManager


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    reply = models.BooleanField(verbose_name='Is a reply?', default=False)

    objects = PostManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})