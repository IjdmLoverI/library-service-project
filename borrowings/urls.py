from django.urls import path
from .views import BorrowingListView, BorrowingDetailView, BorrowingCreateView, ReturnBorrowingView, PaymentListView, \
    PaymentDetailView, PaymentCreateView

urlpatterns = [
    path("borrowings/", BorrowingListView.as_view(), name="borrowing-list"),
    path("borrowings/<int:pk>/", BorrowingDetailView.as_view(), name="borrowing-detail"),
    path("borrowings/create/", BorrowingCreateView.as_view(), name="create-borrowing"),
    path("borrowings/<int:pk>/return/", ReturnBorrowingView.as_view(), name="return-borrowing"),
    path("payments/", PaymentListView.as_view(), name="payments-list"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payments-detail"),
    path("payments/create/", PaymentCreateView.as_view(), name="payments-create")
]

app_name = "borrowings"
