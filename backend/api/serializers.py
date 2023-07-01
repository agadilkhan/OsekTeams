from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import *

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def to_representation(self, instance):
        # Exclude the password field from the returned data
        
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'bio')

class OrderBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    
    class Meta:
        model = OrderBook
        fields = ('id', 'book', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id')

class AddressBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressBook
        fields = ('id', 'user')

class AddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    city = serializers.CharField()
    street = serializers.CharField()
    postcode = serializers.CharField()

class UserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField(required=False, allow_blank=True)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save() 
        return instance
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class BookReviewSerializer(serializers.Serializer):
    user = UserSerializer()
    book = BookSerializer()
    review = ReviewSerializer()