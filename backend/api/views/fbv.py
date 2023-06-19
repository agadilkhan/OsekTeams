from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.serializers import *
from api.models import *

@api_view(['POST'])
def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def category_books(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    books = category.books.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = BookSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        book.delete()
        return Response({'deleted':True}, status=status.HTTP_200_OK)
    
@api_view(['GET']) 
@permission_classes([IsAuthenticated])                                                         
def cart_book_list(request):
    user = request.user
    try:
        cart = user.orders.get(ordered=False)
        books = cart.books.all()
        serializer = OrderBookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist as e: 
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, pk):
    user = request.user
    book = Book.objects.get(id=pk)
    cart = user.orders.filter(ordered=False)
    books = []
    if cart.exists():
        if cart[0].books.filter(book__id=book.id):
            order_book = cart[0].books.get(book__id=book.id)
            order_book.quantity += request.data['quantity']
            order_book.save()
        else:
            order_book = OrderBook.objects.create(book=book, quantity=request.data['quantity'])
            cart[0].books.add(order_book)
        books = cart[0].books.all()
    else:
        new_cart = Order.objects.create(user=user)
        order_book = OrderBook.objects.create(book=book, quantity=request.data['quantity'])
        new_cart.books.add(order_book)
        new_cart.save()
        books = new_cart.books.all()
    serializer = OrderBookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, pk):
    try:
        user = request.user
        order_book = OrderBook.objects.get(id=pk)
        cart = user.orders.get(ordered=False)
        cart.books.remove(order_book)
        order_book.delete() 
        books = cart.books.all()
        serializer = OrderBookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_quantity(request, pk):
    try:
        order_book = OrderBook.objects.get(id=pk)
        quantity = request.data['quantity']
        order_book.quantity = quantity
        order_book.save()
        return Response({'updated':True}, status=status.HTTP_200_OK)
    except OrderBook.DoesNotExist as e:
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PATCH'])
# @permission_classes([IsAuthenticated])
# def user_profile_detail(request):
#     user = request.user
#     try:
#         profile = user.userprofile
#     except UserProfile.DoesNotExist as e:
#         profile = UserProfile.objects.create(
#             user = user,
#             first_name = user.first_name,
#             last_name = user.last_name,
#             email = user.email
#         )

#     if request.method == 'GET':
#         serializer = UserProfileSerializer(profile)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     elif request.method == 'PATCH':
#         profile.first_name = request.data.get('first_name', profile.first_name)
#         profile.last_name = request.data.get('last_name', profile.last_name)
#         profile.email = request.data.get('email', profile.email)
#         profile.phone_number = request.data.get('phone_number', profile.phone_number)
#         profile.save()
#         serializer = UserProfileSerializer(profile)
#         return Response(serializer.data,status=status.HTTP_200_OK )