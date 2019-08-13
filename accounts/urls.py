from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from .views import register_user_view, profile_view, UserPostsView

app_name = "accounts"

urlpatterns = [
    path("register/", register_user_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
    path("my-profile/", profile_view, name="profile"),
    path("password-reset/",
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset_form.html",
             email_template_name='accounts/password_reset_email.html',
             success_url=reverse_lazy('accounts:password_reset_done'),
         ),
         name="password_reset"),
    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy('accounts:password_reset_complete'),
            ),
         name="password_reset_confirm"),
    path('reset-password/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path("<str:username>/", UserPostsView.as_view(), name="user_posts"),
]