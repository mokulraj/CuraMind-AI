from rest_framework.viewsets import ModelViewSet

from .models import (
    Invoice,
    InvoiceItem,
    Payment,
    PaymentTransaction,
    Refund,
)

from .permissions import (
    CanManagePayment,
    CanViewPayment,
    IsPaymentOwner,
)

from .serializers import (
    InvoiceItemSerializer,
    InvoiceSerializer,
    PaymentSerializer,
    PaymentTransactionSerializer,
    RefundSerializer,
)


class InvoiceViewSet(ModelViewSet):
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = (
            Invoice.objects
            .select_related(
                "patient",
                "organization",
            )
            .prefetch_related("items")
            .all()
            .order_by("-created_at")
        )

        if user.is_superuser:
            return queryset

        role = getattr(
            user,
            "role",
            None,
        )

        if role in {
            "ADMIN",
            "STAFF",
            "RECEPTIONIST",
            "FINANCE",
        }:
            return queryset

        if role == "PATIENT":
            patient = getattr(
                user,
                "patient_profile",
                None,
            )

            if patient:
                return queryset.filter(
                    patient=patient
                )

        return queryset.none()

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                CanManagePayment()
            ]

        return [
            CanViewPayment()
        ]


class InvoiceItemViewSet(ModelViewSet):
    queryset = InvoiceItem.objects.all()

    serializer_class = InvoiceItemSerializer

    permission_classes = (
        CanManagePayment,
    )


class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = (
            Payment.objects
            .select_related(
                "invoice",
                "patient",
                "initiated_by",
            )
            .all()
            .order_by("-created_at")
        )

        if user.is_superuser:
            return queryset

        role = getattr(
            user,
            "role",
            None,
        )

        if role in {
            "ADMIN",
            "STAFF",
            "FINANCE",
        }:
            return queryset

        if role == "PATIENT":
            patient = getattr(
                user,
                "patient_profile",
                None,
            )

            if patient:
                return queryset.filter(
                    patient=patient
                )

        return queryset.none()

    def get_permissions(self):
        if self.action in {
            "create",
            "update",
            "partial_update",
            "destroy",
        }:
            return [
                CanManagePayment()
            ]

        return [
            CanViewPayment()
        ]


class PaymentTransactionViewSet(
    ModelViewSet
):
    queryset = (
        PaymentTransaction.objects
        .all()
        .order_by("-created_at")
    )

    serializer_class = (
        PaymentTransactionSerializer
    )

    permission_classes = (
        CanManagePayment,
    )


class RefundViewSet(ModelViewSet):
    queryset = (
        Refund.objects
        .all()
        .order_by("-created_at")
    )

    serializer_class = RefundSerializer

    permission_classes = (
        CanManagePayment,
    )