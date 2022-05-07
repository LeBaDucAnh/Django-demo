from django.urls import path
from .views import *

urlpatterns = [
   path('', index),
   path('search-book', search_book),
   path('borrow-book', borrow_book),
   path('test-post', test_post),
   path('get-user-borrow-list', get_user_borrow_list),
   path('return-book', return_book),
]
