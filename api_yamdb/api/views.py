from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import Token, AccessToken

from reviews.models import Category, Genre, Title, Review, Comments, User
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          CommentsSerializer,
                          ReviewSerializer,
                          UserSerializer,
                          UserTokenSerializer, UserRegSerializer)
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




@api_view(['POST'])
def registration(request):
    serializer = UserRegSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        username = serializer.data.get('username')
        email = serializer.data.get('email')

        #user = User.objects.get_or_create(email=email, username=username)
        user = get_object_or_404(User, email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Ваш код подтверждения',
            f'Ваш код подтверждения: {confirmation_code} \nВаше имя пользователя: {user.username}',
            f'from@example.com',
            ['Yandex@yandex.com',],
            fail_silently=False,
        )
        return Response(serializer.data)
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





