from datetime import date

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


class BorrowingAdminListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email")
    book = serializers.CharField(source="book.title")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingRetrieveSerializer(BorrowingSerializer):
    book = BookSerializer()


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date")
        read_only_fields = ("id", "actual_return_date")

    def validate(self, attrs):
        borrowing = self.instance
        if borrowing.actual_return_date is not None:
            raise serializers.ValidationError(
                "This borrowing has already been returned."
            )
        return attrs

    def update(self, instance, validated_data):
        instance.actual_return_date = date.today()
        instance.book.inventory += 1
        instance.book.save()
        instance.save()
        return instance
