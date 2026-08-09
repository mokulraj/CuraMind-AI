from apps.payments.models import (
    Invoice,
    Payment,
    PaymentTransaction,
    Refund,
)


class PaymentRepository:
    """
    Database access for financial records.
    """

    @staticmethod
    def get_invoice_by_id(
        invoice_id,
    ):
        return (
            Invoice.objects
            .select_related(
                "patient",
                "organization",
            )
            .prefetch_related("items")
            .filter(pk=invoice_id)
            .first()
        )

    @staticmethod
    def get_invoice_by_number(
        invoice_number,
    ):
        return (
            Invoice.objects
            .select_related(
                "patient",
                "organization",
            )
            .prefetch_related("items")
            .filter(
                invoice_number=invoice_number
            )
            .first()
        )

    @staticmethod
    def get_payment_by_id(
        payment_id,
    ):
        return (
            Payment.objects
            .select_related(
                "invoice",
                "patient",
                "initiated_by",
            )
            .filter(pk=payment_id)
            .first()
        )

    @staticmethod
    def get_payment_by_idempotency_key(
        idempotency_key,
    ):
        return (
            Payment.objects
            .filter(
                idempotency_key=idempotency_key
            )
            .first()
        )

    @staticmethod
    def get_payment_by_provider_id(
        provider_payment_id,
    ):
        return (
            Payment.objects
            .filter(
                provider_payment_id=provider_payment_id
            )
            .first()
        )

    @staticmethod
    def list_patient_payments(
        patient_id,
    ):
        return (
            Payment.objects
            .select_related("invoice")
            .filter(
                patient_id=patient_id
            )
            .order_by("-created_at")
        )

    @staticmethod
    def list_transactions(
        payment_id,
    ):
        return (
            PaymentTransaction.objects
            .filter(
                payment_id=payment_id
            )
            .order_by("-created_at")
        )

    @staticmethod
    def list_refunds(
        payment_id,
    ):
        return (
            Refund.objects
            .filter(
                payment_id=payment_id
            )
            .order_by("-created_at")
        )