from rest_framework.routers import DefaultRouter

from .views import (
    InvoiceItemViewSet,
    InvoiceViewSet,
    PaymentTransactionViewSet,
    PaymentViewSet,
    RefundViewSet,
)


app_name = "payments"


router = DefaultRouter()

router.register(
    "invoices",
    InvoiceViewSet,
    basename="invoice",
)

router.register(
    "invoice-items",
    InvoiceItemViewSet,
    basename="invoice-item",
)

router.register(
    "payments",
    PaymentViewSet,
    basename="payment",
)

router.register(
    "transactions",
    PaymentTransactionViewSet,
    basename="transaction",
)

router.register(
    "refunds",
    RefundViewSet,
    basename="refund",
)


urlpatterns = router.urls