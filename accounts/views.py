from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .tasks import send_welcoming_email
from django.contrib.auth import get_user_model
from posts.models import Post
from django.views.generic import ListView


User = get_user_model()


def register_user_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # send_welcoming_email.delay(form.cleaned_data['username'], form.cleaned_data['email'])
            messages.success(request, 'Account created successfully')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/user_register.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Account has been updated')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/profile.html', context)


class UserPostsView(ListView):
    model = Post
    template_name = 'accounts/user_posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['posts'] = Post.objects.filter(user=user)
        context['user'] = user
        return context
