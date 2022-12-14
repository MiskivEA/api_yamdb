from rest_framework import viewsets, permissions
from reviews.models import Category, Genre, Title, Review, Comments, User
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          CommentsSerializer,
                          ReviewSerializer,
                          UserSerializer,
                          UserTokenSerializer)
from .permissions import CommentsReviewPermission


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CommentsReviewPermission]


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [CommentsReviewPermission]

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

