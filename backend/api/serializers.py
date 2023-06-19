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

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class BookSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        if request is not None:
            image_url = request.build_absolute_uri(image_url)
        image_url = f'http://localhost:8000{image_url}'
        return image_url

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
        fields = ('id')

# class AddressBookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AddressBook
#         fields = ('id', 'user', 'addresses')

# class DestinationAddressSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     postcode = serializers.CharField()



class UserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save() 
        return instance