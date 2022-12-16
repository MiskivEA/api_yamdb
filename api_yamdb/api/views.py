
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from reviews.models import Category, Genre, Title, Review, Comments, User
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          CommentsSerializer,
                          ReviewSerializer,
                          UserSerializer,
                          UserTokenSerializer)
from .permissions import CommentsReviewPermission
from rest_framework.generics import CreateAPIView


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    @action(detail=False, url_path='slug')
    def show_category(self, request):
        category = Title.objects.filter(category='slug')
        serializer = self.get_serializer(category, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'

    @action(detail=False, url_path='slug')
    def show_category(self, request):
        genre = Title.objects.filter(category='slug')
        serializer = self.get_serializer(genre, many=True)
        return Response(serializer.data)


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
    # permission_classes = permissions.IsAdminUser


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
