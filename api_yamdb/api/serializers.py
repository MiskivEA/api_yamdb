from rest_framework import serializers
from reviews.models import Category, Genre, Title, Comments, Review, User, GenreTitle


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(read_only=True,
                                         slug_field='slug',
                                         queryset=Category.objects.all(),
                                         )

    class Meta:
        fields = '__all__'
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(many=True,
                                          read_only=True,
                                          slug_field='slug',
                                          queryset=Genre.objects.all(),
                                          )
    # TODO жанров может быть много, категория одна (проверить правильность)
    # TODO изменить отображение str вместо slug
    class Meta:
        fields = '__all__'
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True, default='')
    genre = GenreSerializer(read_only=True, default='Жанр не определен')

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')


class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserTokenSerializer(serializers.ModelSerializer):

    confirmation_code = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
