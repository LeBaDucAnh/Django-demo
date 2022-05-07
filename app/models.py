from django.db import models

# Create your models here.


class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('Category', null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    published_year = models.IntegerField()
    total_qty = models.IntegerField()
    current_qty = models.IntegerField()
    max_duration = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class BookCopy(models.Model):
    class Status:
        AVAILABLE = 1
        BORROWED = 2
        LOST = 3

    barcode = models.CharField(max_length=30, unique=True)
    buy_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.PROTECT)

    def __str__(self):
        return self.barcode


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.fullname


class BoookBorrow(models.Model):
    class Status:
        BORROWING = 1
        RETURNED = 2

    book_copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    borrow_date = models.DateTimeField()
    deadline = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField()
