from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingDetailSerializer


class BorrowingListView(generics.ListAPIView):
    serializer_class = BorrowingDetailSerializer

    def get_queryset(self):
        return Borrowing.objects.filter(user=self.request.user)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
