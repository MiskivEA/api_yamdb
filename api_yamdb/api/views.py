from django.db.models import Avg
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework import viewsets
from rest_framework import permissions


from reviews.models import Category, Genre, Title, Review, Comments, User
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitlePostSerializer,
                          TitleGetSerializer,
                          CommentsSerializer,
                          ReviewSerializer,
                          UserSerializer,
                          UserTokenSerializer, UserRegSerializer)
from .permissions import (CommentsReviewPermission,
                          AnonimUserAdminPermission,
                          AdminOrReadOnly,
                          IsAdminPermission)
from .filters import TitleFilter
from rest_framework.generics import get_object_or_404


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AnonimUserAdminPermission,)

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg('reviews__score'),)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitlePostSerializer
        return TitleGetSerializer


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
    permission_classes = [IsAdminPermission]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)


@action(detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated])
def me(self, request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def registration(request):
    serializer = UserRegSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user = get_object_or_404(User, email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)

        mail = (
            'Подтверждение регистрации',
            f'Ваше имя пользователя: {user.username} \n'
            f'Ваш код подтверждения: {confirmation_code}',
            'from@example.com',
            ['Yandex@yandex.com', ]
        )
        send_mail(*mail, fail_silently=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_code_and_create_token(request):
    serializer = UserTokenSerializer(data=request.data)
    username = serializer.initial_data.get('username')
    confirmation_code = serializer.initial_data.get('confirmation_code')

    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        jwt_token = AccessToken.for_user(user)
        return Response({'token': str(jwt_token)}, status=status.HTTP_200_OK)
    print('ОШИБКА АВТОРИЗАЦИИ - НЕ СОВПАДАЮТ ТОКЕНЫ')
    return Response(status=status.HTTP_400_BAD_REQUEST)
