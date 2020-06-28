"""dev_up URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import confirm_email
from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.social import GithubLogin, GoogleLogin

urlpatterns = [
    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/github/', GithubLogin.as_view(), name='github_login'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('dj-rest-auth/account-confirm-email/', VerifyEmailView.as_view(),
         name='account_email_verification_sent'),
    re_path('auth/registration/confirm/(?P<key>.+)/$',
            confirm_email, name='account_confirm_email'),
]
