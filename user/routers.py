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
from django.urls import include, path
from rest_framework.compat import re_path

from user.social import GithubConnect, GithubLogin, GoogleConnect, GoogleLogin

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/github/', GithubLogin.as_view(), name='github_login'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/github/connect', GithubConnect.as_view(), name='github_connect'),
    path('rest-auth/google/connect', GoogleConnect.as_view(), name='google_connect'),
    re_path('accounts-rest/registration/account-confirm-email/(?P<key>.+)/$',
            confirm_email, name='account_confirm_email'),
]
