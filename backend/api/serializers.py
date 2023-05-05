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
    image = serializers.SerializerMethodField()

    def get_image(self, book):
        request = self.context.get('request')
        host = request.build_absolute_uri('/')[:-1] if request else ''
        image_url = book.image.url if book.image else ''
        return f"{host}{image_url}"

    class Meta:
        model = Book
        fields = '__all__'

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

class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)

    def update(self, request, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance