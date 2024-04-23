from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from books.models import Book
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


class BorrowingCreateSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field='id')

    class Meta:
        model = Borrowing
        fields = (
            "book",
            "borrow_date",
            "expected_return_date"
        )

    def validate(self, attrs):
        book = attrs.get("book")
        if book and book.inventory == 0:
            raise serializers.ValidationError("The inventory of the book is zero.")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        borrower = self.context["request"].user
        book = validated_data.pop("book")

        Book.objects.filter(id=book.id).update(inventory=F("inventory") - 1)
        existing_book = Book.objects.get(id=book.id)

        borrowing = Borrowing.objects.create(
            borrower=borrower, book=existing_book, **validated_data
        )

        return borrowing
