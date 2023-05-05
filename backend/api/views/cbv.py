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

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)


# class CategoryDetailAPIView(mixins.RetrieveModelMixin,
#                             mixins.UpdateModelMixin,
#                             mixins.DestroyModelMixin,
#                             generics.GenericAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     lookup_url_kwarg = 'pk'

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    
class BookListAPIView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    

class BookDetailAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    # def put(self, request, *args, **kwargs):
    #     return self.put(request, *args, **kwargs)
    
    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

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
    def get(self, request):
        permission_classes = (IsAuthenticated, )
        user = request.user
        try:
            address_book = user.addressbook
            serializer = AddressBookSerializer(address_book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AddressBook.DoesNotExist as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        permission_classes = (IsAuthenticated, )
        user = request.user
        city = request.data['city']
        street = request.data['street']
        postcode = request.data['postcode']
        address, created = Address.objects.get_or_create(
            city = city,
            street = street,
            postcode = postcode
        )
        addresses = user.addressbook.addresses
        addresses.add(address)
        serializer = AddressBookSerializer(user.addressbook)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddressDetailAPIView(APIView):
    def get(self, request, pk):
        permsision_classes = (IsAuthenticated, )
        address = Address.objects.get(id=pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def put(self, request, pk):
    #     permission_classes = (IsAuthenticated, )
    #     user = request.user
    #     new_address = Address.objects.get_or_create(
    #         city = request.data['city'],
    #         street = request.data['street'],
    #         postcode = request.data['postcode']
    #     )
    #     addresses = user.addressbook.addresses.all()
    #     serializer = AddressSerializer(addresses, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    