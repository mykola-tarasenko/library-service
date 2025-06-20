from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.CharField(source="book.title")
    user = serializers.CharField(source="user.email")


class BorrowingRetrieveSerializer(BorrowingSerializer):
    book = BookSerializer()
    user = serializers.CharField(source="user.email")
