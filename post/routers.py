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

from django.urls import path, re_path

from post.api.category import CategoryAPI
from post.api.comment import CommentAPI
from post.api.post import PostAPI
from post.api.tag import TagAPI

urlpatterns = [
    path('/categories', CategoryAPI.as_view({'get': 'list'})),
    path('/tags', TagAPI.as_view({'get': 'list'})),
    path('/comments/<int:comment_id>', CommentAPI.as_view({
        'put': 'update',
        'delete': 'destroy',
    })),
    path('/comments', CommentAPI.as_view({
        'post': 'create',
    })),
    path('/<int:post_id>', PostAPI.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    })),
    re_path(r'^$', PostAPI.as_view({
        'get': 'list',
        'post': 'create',
    })),
]
