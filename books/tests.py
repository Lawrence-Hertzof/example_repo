from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
import json
from .models import Book


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            publication_date="2023-01-01",
            pages=200
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.isbn, "1234567890123")
        self.assertEqual(self.book.pages, 200)

    def test_book_str_method(self):
        self.assertEqual(str(self.book), "Test Book")


class BookAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="API Test Book",
            author="API Test Author",
            isbn="9876543210123",
            publication_date="2023-06-01",
            pages=300
        )

    def test_get_book_list(self):
        response = self.client.get('/books/api/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('books', data)
        self.assertEqual(len(data['books']), 1)

    def test_get_book_detail(self):
        response = self.client.get(f'/books/api/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], "API Test Book")
        self.assertEqual(data['author'], "API Test Author")

    def test_create_book(self):
        book_data = {
            'title': 'New Test Book',
            'author': 'New Test Author',
            'isbn': '1111111111111',
            'publication_date': '2023-12-01',
            'pages': 250
        }
        response = self.client.post('/books/api/', 
                                  data=json.dumps(book_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'New Test Book')
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        update_data = {
            'title': 'Updated Test Book',
            'author': 'Updated Test Author',
            'isbn': '9876543210123',
            'publication_date': '2023-06-01',
            'pages': 350
        }
        response = self.client.put(f'/books/api/{self.book.id}/',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Updated Test Book')
        self.assertEqual(data['pages'], 350)

    def test_delete_book(self):
        response = self.client.delete(f'/books/api/{self.book.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 0)

    def test_book_not_found(self):
        response = self.client.get('/books/api/999/')
        self.assertEqual(response.status_code, 404)
