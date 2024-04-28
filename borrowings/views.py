import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing, Payment
from borrowings.permissions import IsAdminOrOwner
from borrowings.serializers import (
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
    ReturnBorrowingSerializer,
    PaymentSerializer
)


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


class ReturnBorrowingView(generics.UpdateAPIView):
    serializer_class = ReturnBorrowingSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        borrowing = self.get_object()
        try:
            borrowing.return_borrowing()
            return Response({"message": "Borrowing returned successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                return Borrowing.objects.filter(borrower_id__in=user_id)
            return Borrowing.objects.all()
        return Borrowing.objects.filter(borrower=self.request.user)


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrOwner]


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrOwner]


stripe.api_key = settings.STRIPE_API_KEY


@require_http_methods(["POST", "GET"])
@csrf_exempt
def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Custom Product',
                    },
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/api/borrowings/borrowings/',
            cancel_url='http://localhost:8000/api/borrowings/payments/',
        )
        return JsonResponse({
            'id': checkout_session.id,
            'url': checkout_session.url
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


