from django.shortcuts import render
from django.views import View
from .models import HashTag


class HashTagView(View):
    def get(self, request, hashtag, *args, **kwargs):
        hashtag = HashTag.objects.get(tag=hashtag)
        posts = hashtag.get_posts()
        return render(request, "hashtags/tag_page.html", {"hashtag": hashtag, "posts": posts})
