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

from user.social import GithubLogin, GoogleLogin

urlpatterns = [
    path('auth/token', obtain_jwt_token, name='token_obtain'),
    path('auth/token/refresh', refresh_jwt_token, name='token_refresh'),
    path('auth/token/verify', verify_jwt_token, name='token_verify'),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('auth/github/', GithubLogin.as_view(), name='github_login'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    re_path('auth/registration/confirm/(?P<key>.+)/$',
            confirm_email, name='account_confirm_email'),
]
