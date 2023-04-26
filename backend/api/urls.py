from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from api import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('registration/', views.register_user),

    path('shop/books/', views.book_list),
    path('shop/books/<int:pk>/', views.book_detail),
    path('shop/categories/', views.CategoryListAPIView),
    path('shop/categories/<int:pk>', views.CategoryDetailAPIView),
]