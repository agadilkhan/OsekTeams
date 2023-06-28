from django.contrib import admin
from api.models import *

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image')

@admin.register(OrderBook)
class OrderBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ordered')
    filter_horizontal = ['books']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'street', 'postcode')

@admin.register(AddressBook)
class AddresBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    filter_horizontal = ['addresses']

@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'order_status', 'ordered_date', 'canceled_date', 'delivered_date')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number')