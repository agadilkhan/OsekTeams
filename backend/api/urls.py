from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from api import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('registration/', views.register_user),

    path('category/<int:pk>/books/', views.category_books),
    path('books/', views.book_list),
    path('books/<int:pk>/', views.book_detail),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('add_to_cart/<int:pk>/', views.add_to_cart),

    path('cart/books/', views.cart_book_list),
    path('cart/remove/<int:pk>/', views.remove_from_cart),
    path('cart/update/<int:pk>/', views.update_quantity),

    path('orders/', views.OrderListAPIView.as_view()),
    path('orders/<int:pk>/', views.OrderDetailAPIView.as_view()),

    path('address_book/', views.AddressBookAPIView.as_view()),
    
    path('addresses/', views.AddressListAPIView.as_view()),
    path('addresses/<int:pk>/', views.AddressDetailAPIView.as_view()),
    path('add_address/', views.add_address),

    path('profile/', views.UserProfileAPIView.as_view()),
]