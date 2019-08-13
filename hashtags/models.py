from django.db import models
from posts.models import Post


class HashTag(models.Model):
    tag = models.CharField(max_length=60)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_posts(self):
        return Post.objects.filter(content__icontains="#" + self.tag)

    class Meta:
        verbose_name_plural = "Hashtags"
