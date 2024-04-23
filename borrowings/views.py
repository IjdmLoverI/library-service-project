from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingDetailSerializer, BorrowingCreateSerializer


class BorrowingListView(generics.ListAPIView):
    serializer_class = BorrowingDetailSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                return Borrowing.objects.filter(borrower_id__in=user_id)
            return Borrowing.objects.all()
        return Borrowing.objects.filter(borrower=self.request.user)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
    permission_classes = [IsAuthenticated]


class BorrowingCreateView(generics.CreateAPIView):
    serializer_class = BorrowingCreateSerializer
    permission_classes = [IsAuthenticated]
