from rest_framework import serializers
from reviews.models import Category, Genre, Title, User


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(read_only=True,
                                         slug_field='titles')

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(many=True,
                                         read_only=True,
                                         slug_field='titles')
    # TODO жанров может быть много, категория одна (проверить правильность)

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    # TODO отображение полей Category и Genre

    class Meta:
        fields = '__all__'
        model = Title


class UserSerializer(serializers.ModelSerializer):

     class Meta:
         model = User
         fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(max_length=6)
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
