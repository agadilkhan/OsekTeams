from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

ORDER_STATUS_CHOICES = [
    ('OR', 'Ordered'),
    ('DE', 'Delivered'),
    ('CA', 'Canceled'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=11, blank=True)

    def __str__(self):
        return f'{self.user} {self.phone_number}'

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='books')

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.name

class Address(models.Model):
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return f'{self.city} {self.street} {self.postcode}'
    
class AddressBook(models.Model):
    addresses = models.ManyToManyField(Address)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'User address'
        verbose_name_plural = 'User addresses'

    
class OrderBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Order book'
        verbose_name_plural = 'Order books'

class Order(models.Model):
    books = models.ManyToManyField(OrderBook)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    ordered = models.BooleanField(default=False)
    destination_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='histories')
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)

    class Meta:
        verbose_name = 'Order history'
        verbose_name_plural = 'Order histories'