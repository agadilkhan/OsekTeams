from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username','email', 'password')

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'category', 'name', 'author', 'description', 'price', 'count')