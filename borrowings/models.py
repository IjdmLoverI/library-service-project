from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import F
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(default=timezone.now)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def clean(self):
        if self.actual_return_date and self.actual_return_date < self.borrow_date:
            raise ValidationError(_("Actual return date cannot be before borrow date."))
        if self.expected_return_date < self.borrow_date:
            raise ValidationError(_("Expected return date cannot be before borrow date."))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expected_return_date = self.borrow_date + timedelta(days=7)
            super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    expected_return_date__gte=models.F('borrow_date')), name='valid_return_date'
            ),
            models.CheckConstraint(
                check=models.Q(
                    actual_return_date__gte=models.F('borrow_date')
                ),
                name='valid_actual_return_date'
            )
        ]

    @property
    def is_active(self) -> bool:
        if not self.actual_return_date:
            return True
        return False

    def return_borrowing(self):
        if self.actual_return_date:
            raise ValueError("This borrowing has already been returned")
        self.actual_return_date = timezone.now()
        self.book.inventory = F("inventory") + 1
        self.book.save()
        self.delete()
