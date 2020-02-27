from django.urls import include, path

# from django.contrib.auth.models import User, Group
# from django.contrib import admin
#
# admin.autodiscover()
#
# from rest_framework import generics, permissions, serializers
# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name')
#
#
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('name',)
#
#
# class UserList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetails(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class GroupList(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated, TokenHasScope]
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

urlpatterns: list = [
    # path('admin', admin.site.urls),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('users/', UserList.as_view()),
    # path('users/<pk>', UserDetails.as_view()),
    # path('group', GroupList.as_view())
]
