from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import *

from api.serializers import *
from api.models import *

@api_view(['POST'])
def register_user(request):
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    email = request.data['email']
    username = request.data['username']
    password = request.data['password']
    try:
        User.objects.create(first_name=first_name, last_name=last_name,
                            email=email, username=username, password=password)
        serializer = UserSerializer(request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
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
def cart_book_list(request):
    permission_classes = (IsAuthenticated, )
    user = request.user
    try:
        cart = user.orders.get(ordered=False)
        books = cart.books.all()
        serializer = OrderBookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist as e: 
        return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_to_cart(request, pk):
    permission_classes = (IsAuthenticated, )
    user = request.user
    book = Book.objects.get(id=pk)
    order_book, created = OrderBook.objects.get_or_create(book=book)
    cart = user.orders.filter(ordered=False)
    if cart.exists():
        if cart[0].books.filter(book__id=book.id).exists():
            order_book.quantity += 1
            order_book.save()
        else:
            cart[0].books.add(order_book)
    else:
        cart = Order.objects.create(user=user, books=order_book)
        cart.books.add(book)
    books = cart[0].books.all()
    serializer = OrderBookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def remove_from_cart(request, pk):
    permission_classes = (IsAuthenticated, )
    user = request.user
    book = Book.objects.get(id=pk)
    order_book = OrderBook.objects.get(book=book)
    cart = user.orders.get(ordered=False)
    cart.books.remove(order_book)
    books = cart.books.all()
    serializer = OrderBookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_quantity(request, pk):
    permission_classes = (IsAuthenticated, )
    user = request.user
    order_book = OrderBook.objects.get(id=pk)
    quantity = request.data['quantity']
    order_book.quantity = quantity
    order_book.save()
    return Response({'updated':True}, status=status.HTTP_200_OK)

@api_view(['GET', 'PATCH'])
def user_profile_detail(request):
    permission_classes = (IsAuthenticated, )
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist as e:
        profile = UserProfile.objects.create(
            user = user,
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email
        )

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':
        profile.first_name = request.data.get('first_name', profile.first_name)
        profile.last_name = request.data.get('last_name', profile.last_name)
        profile.email = request.data.get('email', profile.email)
        profile.phone_number = request.data.get('phone_number', profile.phone_number)
        profile.save()
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data,status=status.HTTP_200_OK )