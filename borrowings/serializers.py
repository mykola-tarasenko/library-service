from django.db import transaction
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
        read_only_fields = ("id", "actual_return_date")

    def validate_book(self, book):
        if book.inventory < 1:
            raise serializers.ValidationError("Book is out of stock.")
        return book

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data["book"]
            book.inventory -= 1
            book.save()

            borrowing = Borrowing.objects.create(**validated_data)
            return borrowing


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.CharField(source="book.title")


class BorrowingRetrieveSerializer(BorrowingSerializer):
    book = BookSerializer()


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date")
        read_only_fields = ("id", "actual_return_date")
