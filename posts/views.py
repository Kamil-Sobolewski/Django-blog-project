from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView
from .forms import PostModelForm
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'posts/homepage.html'
    context_object_name = 'posts'
    paginate_by = 5
    queryset = Post.objects.filter(parent=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostModelForm()
        context['action_url'] = reverse_lazy('posts:create')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('posts:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    template_name = 'posts/post_reply.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.reply = True
        obj.user = self.request.user
        obj.parent = Post.objects.get(pk=self.kwargs.get('pk'))
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:detail', kwargs={'pk': self.kwargs.get('pk')})


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostModelForm()
        context['action_url'] = reverse_lazy('posts:reply', kwargs={'pk': self.object.id})
        return context


@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.user == request.user:
        if request.method == 'POST':
            post.delete()
            return redirect(reverse_lazy('posts:home'))
    else:
        raise PermissionDenied

    context = {'post': post}

    return render(request, 'posts/post_delete.html', context)


@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.user == request.user:
        if request.method != 'POST':
            # Initial request; pre-fill form with the current post info
            form = PostModelForm(instance=post)
        else:
            # POST data submitted; process data
            form = PostModelForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect(post)
    else:
        raise PermissionDenied

    context = {'form': form}

    return render(request, 'posts/post_edit_form.html', context)

