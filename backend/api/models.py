from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    count = models.IntegerField()

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'