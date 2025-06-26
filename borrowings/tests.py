from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer, BorrowingAdminListSerializer

BORROWING_URL = reverse("borrowings:borrowing-list")


def detail_url(borrowing_id: int):
    return reverse("borrowings:borrowing-detail", args=[borrowing_id])


def return_url(borrowing_id: int):
    return reverse("borrowings:borrowing-return-borrowing", args=[borrowing_id])


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


class BorrowingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.staff_user = get_user_model().objects.create_user(
            email="admin@example.com", password="adminpass123", is_staff=True
        )
        self.book = Book.objects.create(
            title="Book",
            author="Author",
            cover="SOFT",
            inventory=3,
            daily_fee=0.50,
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=3),
        )

    def test_borrowing_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(BORROWING_URL)
        serializer = BorrowingListSerializer(self.borrowing)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], serializer.data)

    def test_borrowing_list_for_admin(self):
        Borrowing.objects.create(
            book=self.book,
            user=self.staff_user,
            borrow_date=date.today(),
            expected_return_date=date.today() + timedelta(days=5),
        )
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(BORROWING_URL)
        borrowings = Borrowing.objects.all()
        serializer = BorrowingAdminListSerializer(borrowings, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(serializer.data, response.data)

    def test_borrowing_create(self):
        self.client.force_authenticate(self.user)
        payload = {
            "book": self.book.id,
            "borrow_date": date.today(),
            "expected_return_date": date.today() + timedelta(days=7),
        }
        response = self.client.post(BORROWING_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 2)

    def test_borrowing_create_with_no_inventory_fails(self):
        self.book.inventory = 0
        self.book.save()
        self.client.force_authenticate(self.user)
        payload = {
            "book": self.book.id,
            "borrow_date": date.today(),
            "expected_return_date": date.today() + timedelta(days=2),
        }
        response = self.client.post(BORROWING_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Book is out of stock", str(response.data))

    def test_retrieve_borrowing(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(detail_url(self.borrowing.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["book"]["id"], self.book.id)

    def test_borrowing_return_success(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(return_url(self.borrowing.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.borrowing.refresh_from_db()
        self.book.refresh_from_db()
        self.assertIsNotNone(self.borrowing.actual_return_date)
        self.assertEqual(self.book.inventory, 4)

    def test_borrowing_return_twice_fails(self):
        self.borrowing.actual_return_date = date.today()
        self.borrowing.save()
        self.client.force_authenticate(self.user)
        response = self.client.post(return_url(self.borrowing.id))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already been returned", str(response.data))
