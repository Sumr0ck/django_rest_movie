from rest_framework import serializers

from .models import Movie, Review


class FilterReviewSerializer(serializers.ListSerializer):
    """Фильтр комментариев: только parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""
    actors = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'actors')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewSerializer
        model = Review
        fields = ('id', 'email', 'name', 'text', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полный фильм"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    genres = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True)
    directors = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft', )
