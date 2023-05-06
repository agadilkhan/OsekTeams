from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from api import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('registration/', views.register_user),

    path('shop/category/<int:pk>/books/', views.category_books),
    path('shop/books/', views.book_list),
    path('shop/books/<int:pk>/', views.book_detail),
    path('shop/categories/', views.CategoryListAPIView.as_view()),
    path('shop/add_to_cart/<int:pk>/', views.add_to_cart),

    path('cart/books/', views.cart_book_list),
    path('cart/remove/<int:pk>/', views.remove_from_cart),
    path('cart/update/<int:pk>/', views.update_quantity),

    path('orders/', views.OrderListAPIView.as_view()),
    path('orders/<int:pk>/', views.OrderDetailAPIView.as_view()),
    path('address_book/', views.AddressBookAPIView.as_view()),
    path('address_book/<int:pk>/', views.AddressDetailAPIView.as_view()),

    path('profile/', views.user_profile_detail),
]