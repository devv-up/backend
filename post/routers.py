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

from django.urls import path

from post.api.category import CategoryAPI
from post.api.post import PostAPI
from post.api.tag import TagAPI

urlpatterns = [
    path('categories/<int:category_id>', CategoryAPI.as_view()),
    path('categories', CategoryAPI.as_view()),
    path('tags/<int:tag_id>', TagAPI.as_view()),
    path('tags', TagAPI.as_view()),
    path('posts/<int:post_id>', PostAPI.as_view()),
    path('posts', PostAPI.as_view()),
]
