from django.urls import path

from rest_framework.routers import SimpleRouter

from dashboard.views import (
    CustomerViewSet,
    PaymentViewSet,
    CustomerPaymentListView,
)


app_name = "dashboard"

router = SimpleRouter()
router.register(r"customer", CustomerViewSet, basename="customer")
router.register(r"payment", PaymentViewSet, basename="payment")

urlpatterns = [
    path(
        "customer/<str:customer_id>/payment/",
        CustomerPaymentListView.as_view(),
        name="customer-payment-list",
    ),
]

urlpatterns += router.urls
