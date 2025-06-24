from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.CharField(source="book.title")


class BorrowingRetrieveSerializer(BorrowingSerializer):
    book = BookSerializer()
