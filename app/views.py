from .models import *
from django.shortcuts import render
from django.shortcuts import HttpResponse
import json
from django.db.models import Q
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def index(request):
    return render(request, 'index.html')


def search_book(request):
    params = request.GET
    keyword = params.get('keyword', '')
    category_id = params.get('category_id')
    start_year = params.get('start_year')
    end_year = params.get('end_year')
    books = Book.objects.all()

    if keyword != '':
        books = books.filter(
            Q(name__icontains=keyword) |
            Q(isbn__icontains=keyword)
        )
    if category_id:
        books = books.filter(category__id=category_id)
    if start_year:
        books = books.filter(
            published_year__gt=start_year,
        )
    if end_year:
        books = books.filter(
            published_year__lt=end_year,
        )
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'name': book.name,
            'isbn': book.isbn,
            'author': book.author.name,
            'available': book.current_qty > 0,
        })
    return HttpResponse(json.dumps(result))


@csrf_exempt
def borrow_book(request):
    body = request.POST
    username = body.get('username')
    barcode = body.get('barcode')

    user = User.objects.filter(username=username).first()
    book_copy = BookCopy.objects.filter(barcode=barcode).first()

    if not user:
        return HttpResponse(json.dumps({'error': 'Người dùng không tồn tại'}))
    if not book_copy:
        return HttpResponse(json.dumps({'error': 'Barcode không hợp lệ'}))

    book_borrow = BoookBorrow()
    book_borrow.user = user
    book_borrow.book_copy = book_copy
    book_borrow.borrow_date = datetime.now()
    book_borrow.deadline = datetime.now() + timedelta(days=book_copy.book.max_duration)
    book_borrow.status = BoookBorrow.Status.BORROWING
    book_borrow.save()

    book_copy.status = BookCopy.Status.BORROWED
    book_copy.save()

    book_copy.book.current_qty -= 1
    book_copy.book.save()

    return HttpResponse(json.dumps({'success': True}))


@csrf_exempt
def test_post(request):
    body = request.POST  # {'username': 'nguyenvana'}
    username = body.get('username', '')
    return HttpResponse(f"Hello {username}")


def get_user_borrow_list(request):
    params = request.GET
    username = params.get('username')
    lst = BoookBorrow.objects.filter(
        user__username=username
    )
    result = []
    for item in lst:
        result.append({
            'borrow_date': item.borrow_date.strftime('%d/%m/%Y %H:%M:%S'),
            'book': item.book_copy.book.name
        })
    return HttpResponse(json.dumps(result))


@csrf_exempt
def return_book(request):
    body = request.POST
    barcode = body.get('barcode')
    book_borrow = BoookBorrow.objects.filter(
        book_copy__barcode=barcode,
        status=BoookBorrow.Status.BORROWING
    ).first()

    if not book_borrow:
        return HttpResponse(json.dumps({'error': 'Sách đã trả'}))

    book_borrow.status = BoookBorrow.Status.RETURNED
    book_borrow.save()

    book_borrow.book_copy.status = BookCopy.Status.AVAILABLE
    book_borrow.book_copy.save()

    book_borrow.book_copy.book.current_qty += 1
    book_borrow.book_copy.book.save()

    return HttpResponse(json.dumps({'success': True}))
