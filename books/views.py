from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Book


def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/list.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/detail.html', {'book': book})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def book_api_list(request):
    if request.method == 'GET':
        books = list(Book.objects.values())
        return JsonResponse({'books': books})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        book = Book.objects.create(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            publication_date=data['publication_date'],
            pages=data['pages']
        )
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'publication_date': book.publication_date.isoformat(),
            'pages': book.pages
        }, status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def book_api_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'publication_date': book.publication_date.isoformat(),
            'pages': book.pages,
            'created_at': book.created_at.isoformat(),
            'updated_at': book.updated_at.isoformat()
        })
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.isbn = data.get('isbn', book.isbn)
        book.publication_date = data.get('publication_date', book.publication_date)
        book.pages = data.get('pages', book.pages)
        book.save()
        
        return JsonResponse({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'publication_date': book.publication_date.isoformat(),
            'pages': book.pages
        })
    
    elif request.method == 'DELETE':
        book.delete()
        return JsonResponse({'message': 'Book deleted successfully'}, status=204)
