from rest_framework import serializers
from categories.models import Category, Similarity


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "image", "parent"]


class SimilaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Similarity
        fields = ["first", "second"]
