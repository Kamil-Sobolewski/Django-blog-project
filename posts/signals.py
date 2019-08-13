from django.db.models.signals import post_save
from django.dispatch import receiver
import re
from .models import Post
from hashtags.models import HashTag


@receiver(post_save, sender=Post)
def create_hashtag_signal(sender, instance, created, **kwargs):
    if created:
        pattern = r"#(\w+)"
        post_content = instance.content
        tags = re.findall(pattern, post_content)
        for tag in tags:
            obj, created = HashTag.objects.get_or_create(tag=tag)