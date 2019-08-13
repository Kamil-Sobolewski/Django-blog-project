from django.views.generic import ListView
from posts.models import Post


class SearchView(ListView):
    template_name = "search/search_page.html"
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Post.objects.search_content(query)
        return Post.objects.none()
