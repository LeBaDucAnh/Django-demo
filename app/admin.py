from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Country)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(User)
admin.site.register(BoookBorrow)

