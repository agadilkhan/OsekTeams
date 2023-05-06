from rest_framework import generics, mixins, status
from rest_framework.permissions import *
from rest_framework.views import APIView, Response

from api.models import *
from api.serializers import *


class CategoryListAPIView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class OrderListAPIView(APIView):
    def get(self, request):
        permission_classes = (IsAuthenticated, )
        user = request.user
        orders = user.orders.filter(ordered=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        permission_classes = (IsAuthenticated, )
        user = request.user
        order = user.orders.get(id=pk)
        books = order.books.all()
        serializer = OrderBookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddressBookAPIView(APIView):
    def get_object(self, request):
        user = request.user
        try:
            address_book = user.addressbook
        except AddressBook.DoesNotExist as e:
            address_book = AddressBook.objects.create(
                user=user
            )
        return address_book
    
    def get(self, request):
        permission_classes = (IsAuthenticated, )
        address_book = self.get_object(request)
        serializer = AddressBookSerializer(address_book)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        permission_classes = (IsAuthenticated, )
        address_book = self.get_object(request)
        city = request.data['city']
        street = request.data['street']
        postcode = request.data['postcode']
        address, created = Address.objects.get_or_create(
            city = city,
            street = street,
            postcode = postcode
        )
        address_book.addresses.add(address)
        serializer = AddressBookSerializer(address_book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddressDetailAPIView(APIView):
    def get(self, request, pk):
        permsision_classes = (IsAuthenticated, )
        address = Address.objects.get(id=pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)