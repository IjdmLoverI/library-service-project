from django.urls import path
from .views import BorrowingListView, BorrowingDetailView, BorrowingCreateView

urlpatterns = [
    path("borrowings/", BorrowingListView.as_view(), name="borrowing-list"),
    path("borrowings/<int:pk>/", BorrowingDetailView.as_view(), name="borrowing-detail"),
    path("borrowings/create/", BorrowingCreateView.as_view(), name="create-borrowing"),
]

app_name = "borrowings"
