from django.db import models
from django.forms import ChoiceField


class Book(models.Model):
    COVER_CHOICES = (
        ("HARD", "Hard cover"),
        ("SOFT", "Soft cover")
    )
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField(default=0)
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
