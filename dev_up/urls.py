from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('member.urls'), name='member'),
    path('', include('meeting_board.routers'), name='meeting_board'),
]
