from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.utils import timezone

ORDER_STATUS_CHOICES = [
    ('OR', 'Ordered'),
    ('DE', 'Delivered'),
    ('CA', 'Canceled'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True)

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    def __str__(self):
        return f'{self.user} {self.phone_number}'

# when a new user is created, his profile is created
def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance, first_name=instance.first_name,
                                                 last_name=instance.last_name, email=instance.email)

post_save.connect(userprofile_receiver, User)

# when we update the profile, then the user is updated
@receiver(post_save, sender=UserProfile)
def update_user(sender, instance, created, **kwargs):
    instance.user.first_name = instance.first_name
    instance.user.last_name = instance.last_name
    instance.user.email = instance.email
    instance.user.save()

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
        return f'{self.category} {self.name}' 

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
    
    def __str__(self):
        return f'{self.addresses} {self.user}'

# when a new user is created, his addressbook is created
def addressbook_receiver(sender, instance, created, *args, **kwargs):
    if created:
        addressbook = AddressBook.objects.create(user=instance)

post_save.connect(addressbook_receiver, User)

    
class OrderBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Order book'
        verbose_name_plural = 'Order books'
    
    def __str__(self):
        return f'{self.book} {self.quantity}'
    
    def get_total_price(self):
        return self.book.price * self.quantity

class Order(models.Model):
    books = models.ManyToManyField(OrderBook)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    ordered = models.BooleanField(default=False)
    destination_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'order_id: {self.id}, user: {self.user}'

    def clean(self):
        # destination_address field is required if ordered=True
        if self.ordered and not self.destination_address:
            raise ValidationError("Destination address is required when ordered is True.")
    
    def get_total_price(self):
        total = 0
        for book in self.books.all():
            total += book.get_total_price()

        return total

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='histories')
    ordered_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    canceled_date = models.DateTimeField(null=True, blank=True)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)

    class Meta:
        verbose_name = 'Order history'
        verbose_name_plural = 'Order histories'
    
    def __str__(self):
        return f'{self.order} {self.order_status}'

@receiver(pre_save, sender=OrderHistory)
def set_order_dates(sender, instance, **kwargs):
    if (instance.order_status == 'Ordered' or instance.order_status == 'OR') and not instance.ordered_date:
        instance.ordered_date = timezone.now()
    elif (instance.order_status == 'Canceled' or instance.order_status == 'CA') and not instance.canceled_date:
        instance.canceled_date = timezone.now()
    elif (instance.order_status == 'Delivered' or instance.order_status == 'DE')and not instance.delivered_date:
        instance.delivered_date = timezone.now()