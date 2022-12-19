from rest_framework import viewsets, filters, mixins, status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.core.mail import send_mail


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


class MyViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class CategoryViewSet(MyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(MyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleGetSerializer
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
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [CommentsReviewPermission]

    def get_queryset(self):
        """Возращает кверисет c комментами для отзыва"""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Создание коммента к отзыву текущего юзера"""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.ListModelMixin, mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminPermission]
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def registration(request):
    serializer = UserRegSerializer(data=request.data)
    if request.data.get('username') == 'me':
        return Response(status=status.HTTP_400_BAD_REQUEST)
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
            [user.email, ]
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
