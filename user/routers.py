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
from django.urls import include, path, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from user.social import GithubConnect, GithubLogin, GoogleConnect, GoogleLogin

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('token/auth/', obtain_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('token/verify/', verify_jwt_token),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('auth/github/', GithubLogin.as_view(), name='github_login'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/github/connect', GithubConnect.as_view(), name='github_connect'),
    path('auth/google/connect', GoogleConnect.as_view(), name='google_connect'),
    re_path('accounts-rest/registration/account-confirm-email/(?P<key>.+)/$',
            confirm_email, name='account_confirm_email'),
]
