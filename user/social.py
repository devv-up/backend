
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialConnectView, SocialLoginView


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/user/accounts/github/login/callback/"
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/user/accounts/google/login/callback/"
    client_class = OAuth2Client


class GithubConnect(SocialConnectView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/user/accounts/github/login/callback/"
    client_class = OAuth2Client


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/user/accounts/google/login/callback/"
    client_class = OAuth2Client
