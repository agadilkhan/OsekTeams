from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

ORDER_STATUS_CHOICES = [
    ('OR', 'Ordered'),
    ('DE', 'Delivered'),
    ('CA', 'Canceled'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=True)

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

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
        return f'category: {self.category}, name: {self.name}' 

# class DestinationAddress(models.Model):
#     postcode = models.CharField(max_length=50)

#     class Meta:
#         verbose_name = 'Destination address'
#         verbose_name_plural = 'Destination addresses'
    
#     def __str__(self):
#         return f'{self.postcode}'
    
# class AddressBook(models.Model):
#     addresses = models.ManyToManyField(DestinationAddress)
#     user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         verbose_name = 'User address'
#         verbose_name_plural = 'User addresses'
    
#     def __str__(self):
#         return f'{self.addresses} {self.user}'

    
class OrderBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Order book'
        verbose_name_plural = 'Order books'
    
    def __str__(self):
        return f'{self.book}, quantity: {self.quantity}'

class Order(models.Model):
    books = models.ManyToManyField(OrderBook)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    ordered = models.BooleanField(default=False)
    # destination_address = models.ForeignKey(DestinationAddress, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def clean(self):
        # destination_address field is required if ordered=True
        if self.ordered and not self.destination_address:
            raise ValidationError("Destination address is required when ordered is True.")

    def __str__(self):
        return f'{self.books} {self.user} {self.ordered}'

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='histories')
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)

    class Meta:
        verbose_name = 'Order history'
        verbose_name_plural = 'Order histories'
    
    def __str__(self):
        return f'{self.order} {self.status}'