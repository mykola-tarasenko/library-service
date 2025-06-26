from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer

BOOK_URL = reverse("books:book-list")


def detail_url(book_id: int):
    return reverse("books:book-detail", args=[book_id])


class BookTest(TestCase):
    def test_str_method(self):
        book = Book.objects.create(
            title="Test",
            author="Test Testenko",
            cover="SOFT",
            inventory=2,
            daily_fee=0.02,
        )
        self.assertEqual(
            str(book),
            f"{book.title} by {book.author} ({book.cover})",
        )


class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="test123user", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_book_list(self):
        for i in range(5):
            Book.objects.create(
                title=f"Test{i}",
                author="Test Testenko",
                cover="SOFT",
                inventory=2,
                daily_fee=0.02,
            )

        response = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_book_create(self):
        payload = {
            "title": "Test",
            "author": "Testenko",
            "cover": "SOFT",
            "inventory": 2,
            "daily_fee": "0.05",
        }
        response = self.client.post(BOOK_URL, payload)
        book = Book.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(book.title, payload["title"])
        self.assertEqual(book.author, payload["author"])
        self.assertEqual(book.cover, payload["cover"])
        self.assertEqual(book.inventory, payload["inventory"])
        self.assertEqual(book.daily_fee, Decimal(payload["daily_fee"]))

    def test_book_retrieve(self):
        book = Book.objects.create(
            title=f"Test",
            author="Test Testenko",
            cover="SOFT",
            inventory=2,
            daily_fee=0.02,
        )
        response = self.client.get(detail_url(book.id))
        serializer = BookSerializer(book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_book_partial_update(self):
        payload = {"title": "TEST"}
        book = Book.objects.create(
            title=f"Test",
            author="Test Testenko",
            cover="SOFT",
            inventory=2,
            daily_fee=0.02,
        )
        response = self.client.patch(detail_url(book.id), payload)
        book = Book.objects.get(pk=book.id)
        serializer = BookSerializer(book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_book_update(self):
        payload = {
            "title": "TEST",
            "author": "Testenko",
            "cover": "SOFT",
            "inventory": 2,
            "daily_fee": "0.05",
        }
        book = Book.objects.create(
            title=f"Test",
            author="Test Testenko",
            cover="SOFT",
            inventory=2,
            daily_fee=0.02,
        )
        response = self.client.patch(detail_url(book.id), payload)
        book = Book.objects.get(pk=book.id)
        serializer = BookSerializer(book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
