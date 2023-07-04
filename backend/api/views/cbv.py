from rest_framework import generics, mixins, status
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.models import *
from api.serializers import *


class CategoryListAPIView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class AuthorDetailAPIView(mixins.RetrieveModelMixin,
                          generics.GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class OrderListAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        orders = user.orders.filter(ordered=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        user = request.user
        try:
            order = user.orders.get(id=pk)
            books = order.books.all()
            serializer = OrderBookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        user_profile = user.userprofile
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
    def put(self, request):
        user = request.user
        user_profile = user.userprofile
        serializer = UserProfileSerializer(instance=user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddressBookAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        user = request.user
        address_book = user.addressbook
        serializer = AddressBookSerializer(address_book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddressListAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        addresses = user.addressbook.addresses.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        city, street, postcode = request.data['city'], request.data['street'], request.data['postcode']
        address, created = Address.objects.get_or_create(city=city, street=street, postcode=postcode)
        addresses = user.addressbook.addresses
        addresses.add(address)
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddressDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, request, pk):
        user = request.user
        addresses = user.addressbook.addresses.all()
        try: 
            return addresses.get(id=pk)
        except Address.DoesNotExist as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk):
        address = self.get_object(request, pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        address = self.get_object(request, pk)
        addresses = list(request.user.addressbook.addresses.all())
        index = addresses.index(address)
        updated_address, created = Address.objects.get_or_create(city=request.data['city'], 
                                                  street=request.data['street'], postcode=request.data['postcode'])
        addresses[index] = updated_address
        request.user.addressbook.addresses.set(addresses)
        serializer = AddressSerializer(updated_address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        address = self.get_object(request, pk)
        request.user.addressbook.addresses.remove(address)
        return Response({'deleted':True}, status=status.HTTP_200_OK)  

class BookReviewDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, book_id, book_review_id):
        try:
            book = Book.objects.get(id=book_id)
            book_review = book.reviews.get(id=book_review_id)
            serializer = BookReviewSerializer(book_review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except BookReview.DoesNotExist as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, book_id, book_review_id):
        try:
            book = Book.objects.get(id=book_id)
            book_review = book.reviews.get(id=book_review_id)
            if request.user == book_review.user:
                book_review.review.title = request.data['title']
                book_review.review.content = request.data['content']
                book_review.save()
                serializer = BookReviewSerializer(book_review)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error':'This user cannot edit this review.'}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except BookReview.DoesNotExist as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, book_id, book_review_id):
        try:
            book = Book.objects.get(id=book_id)
            book_review = book.reviews.get(id=book_review_id)
            if request.user == book_review.user:
                book_review.delete()
                return Response({'deleted':True}, status=status.HTTP_200_OK)
            return Response({'error':'This user cannot delete this review.'}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except BookReview.DoesNotExist as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()