from django.http import Http404
from rest_framework import viewsets, permissions, generics

from core.models import Customer, Payment
from dashboard.serializers import (
    CustomerSerializer,
    CreatePaymentSerializer,
    PaymentSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    """Customer Create, Retrieve, Update, List and Delete View"""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "customer_id"
    my_tags = ["Customer"]


class PaymentViewSet(viewsets.ModelViewSet):
    """Payment Create, Retrieve and List view"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    create_serializer_class = CreatePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = [
        "get",
        "post",
    ]
    lookup_field = "payment_ref"
    my_tags = ["Payment"]

    def get_serializer_class(self):
        """Set serializer class to create_serializer_class for create"""
        if self.action == "create":
            if hasattr(self, "create_serializer_class"):
                return self.create_serializer_class

        return super(PaymentViewSet, self).get_serializer_class()


class CustomerPaymentListView(generics.ListAPIView):
    """Retrieves a Customer's payment history"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "customer_id"
    my_tags = ["Customer Payment"]

    def get_queryset(self):
        """Returns a queryset of payments where customer_id is lookup_field"""

        if self.lookup_field is None:
            raise Http404

        customer_id = self.kwargs[self.lookup_field]
        return Payment.objects.filter(customer__customer_id=customer_id)
