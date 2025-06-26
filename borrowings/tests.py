from django.contrib.auth import get_user_model
from django.test import TestCase

from books.models import Book
from borrowings.models import Borrowing


class BorrowingTest(TestCase):
    def test_str_method(self):
        book = Book.objects.create(
            title=f"Test",
            author="Test Testenko",
            cover="SOFT",
            inventory=2,
            daily_fee=0.02,
        )
        user = get_user_model().objects.create_user(
            email=f"test@example.com",
            password="1qazcde3",
        )
        borrowing = Borrowing.objects.create(
            borrow_date="2025-5-1",
            expected_return_date="2025-5-10",
            actual_return_date="2025-6-1",
            book=book,
            user=user,
        )
        self.assertEqual(
            str(borrowing),
            f'{borrowing.user} borrowed "{borrowing.book}" on {borrowing.borrow_date}',
        )
