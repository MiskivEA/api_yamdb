from rest_framework import viewsets
from reviews.models import Category, Genre, Title, Review, Comments, User
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          CommentsSerializer,
                          ReviewSerializer,
                          UserSerializer,
                          UserTokenSerializer)
from .permissions import CommentsReviewPermission
from rest_framework.generics import CreateAPIView, get_object_or_404


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

    def get_queryset(self):
        """Возращает кверисет c отзывами для тайтла"""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создание отзыва для тайтла,
        где автором является текущий пользователь."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [CommentsReviewPermission]

    def get_queryset(self):
        """Возращает кверисет c комментами для отзыва"""
        review = get_object_or_404(Title, pk=self.kwargs.get('review_id'))
        return review.reviews.all()

    def perform_create(self, serializer):
        """Создание коммента к отзыву текущего юзера"""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


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
