from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView

from reviews.models import Category, Genre, Title, User
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, UserSerializer, UserTokenSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = permissions.IsAdminUser


class UserRegistration(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
    def perform_create(self, serializer):
        Тут наверное реализовать отпрвку сообщений
        pass
"""

class ConfirmationCode(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTokenSerializer

    def perform_create(self, serializer):
        pass