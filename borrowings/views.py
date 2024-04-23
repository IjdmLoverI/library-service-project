from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingDetailSerializer


class BorrowingListView(generics.ListAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
