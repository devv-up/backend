
import os

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView

SITE_URL = os.environ.get("SITE_URL", "http://127.0.0.1:8000")


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = f'{SITE_URL}/user/accounts/github/login/callback/'
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = f'{SITE_URL}/user/accounts/google/login/callback/'
    client_class = OAuth2Client
