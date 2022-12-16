from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from django.core.mail import send_mail
from rest_framework.response import Response

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
            f'Ваш код подтверждения: {confirmation_code}',
            f'from@example.com',
            ['Yandex@yandex.com',],
            fail_silently=False,
        )
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
class UserRegistration(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegSerializer



    def perform_create(self, serializer):
        Тут наверное реализовать отпрfвку сообщений
        send_mail(
            'Тема письма', #code
            'Текст письма.', #code
            'from@example.com',  # Это поле "От кого"
            ['to@example.com'],  # Это поле "Кому"
            fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
        )
        serializer.save()


class ConfirmationCode(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTokenSerializer

    def perform_create(self, serializer):
        а тут генеарция токена и как то его нужно еще отдать"""
