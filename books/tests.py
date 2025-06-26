from django.test import TestCase

from books.models import Book


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
