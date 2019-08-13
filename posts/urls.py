from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView, post_delete_view, post_edit_view, ReplyCreateView

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path("create/", PostCreateView.as_view(), name="create"),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path("<int:pk>/delete/", post_delete_view, name="delete"),
    path("<int:pk>/edit/", post_edit_view, name="edit"),
    path("<int:pk>/reply/", ReplyCreateView.as_view(), name="reply"),
]