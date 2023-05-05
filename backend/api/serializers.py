from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import *

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
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
        fields = ('id', 'category', 'name', 'author', 'description', 'price')

class OrderBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    
    class Meta:
        model = OrderBook
        fields = ('id', 'book', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'destination_address')

class AddressBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressBook
        fields = ('id', 'user', 'addresses')

class AddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    city = serializers.CharField()
    street = serializers.CharField()
    postcode = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.city = validated_data.get('city', instance.city)
        instance.street = validated_data.get('street', instance.street)
        instance.postode = validated_data.get('postcode', instance.postcode)
        instance.save()
        return instance