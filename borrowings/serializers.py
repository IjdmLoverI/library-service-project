from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing
from users.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrower",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date"
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    borrower = serializers.CharField(source="borrower.email")
    book = serializers.CharField(source="book.title")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrower",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date"
        )
