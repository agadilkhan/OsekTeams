from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from api import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('registration/', views.register_user),

    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:pk>/books/', views.category_books),

    path('authors/<int:pk>/', views.AuthorDetailAPIView.as_view()),
    path('authors/<int:pk>/books/', views.author_books),

    path('books/', views.book_list),
    path('books/<int:pk>/', views.book_detail),

    path('add_to_cart/<int:pk>/', views.add_to_cart),
    path('cart/', views.cart_book_list),
    path('cart/<int:pk>/remove/', views.remove_from_cart),
    path('cart/<int:pk>/update/', views.update_quantity),

    path('orders/', views.OrderListAPIView.as_view()),
    path('orders/<int:pk>/', views.OrderDetailAPIView.as_view()),

    path('books/<int:pk>/reviews/', views.book_reviews),
    path('books/<int:pk>/reviews/create/', views.create_review),
    
    path('addresses/', views.AddressListAPIView.as_view()),
    path('addresses/<int:pk>/', views.AddressDetailAPIView.as_view()),

    path('profile/', views.UserProfileAPIView.as_view()),
]