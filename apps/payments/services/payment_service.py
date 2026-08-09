from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.payments.models import (
    Invoice,
    Payment,
    PaymentStatus,
)


class PaymentService:
    """
    Payment business operations.

    Provider-specific API calls are intentionally not placed here.
    Provider adapters will be added later.
    """

    @staticmethod
    @transaction.atomic
    def create_payment(
        *,
        invoice,
        patient,
        initiated_by,
        provider,
        method,
        amount,
        idempotency_key,
        metadata=None,
    ):
        amount = Decimal(str(amount))

        if amount <= Decimal("0.00"):
            raise ValueError(
                "Payment amount must be greater than zero."
            )

        if patient.pk != invoice.patient_id:
            raise ValueError(
                "Payment patient does not match invoice patient."
            )

        existing = Payment.objects.filter(
            idempotency_key=idempotency_key,
        ).first()

        if existing:
            return existing

        if amount > invoice.amount_due:
            raise ValueError(
                "Payment amount cannot exceed invoice amount due."
            )

        return Payment.objects.create(
            invoice=invoice,
            patient=patient,
            initiated_by=initiated_by,
            provider=provider,
            method=method,
            amount=amount,
            currency=invoice.currency,
            idempotency_key=idempotency_key,
            metadata=metadata or {},
        )

    @staticmethod
    @transaction.atomic
    def mark_payment_success(
        *,
        payment,
        provider_payment_id,
    ):
        if payment.status == PaymentStatus.SUCCESS:
            return payment

        payment.status = PaymentStatus.SUCCESS
        payment.provider_payment_id = (
            provider_payment_id
        )
        payment.paid_at = timezone.now()

        payment.save(
            update_fields=[
                "status",
                "provider_payment_id",
                "paid_at",
                "updated_at",
            ]
        )

        invoice = (
            Invoice.objects
            .select_for_update()
            .get(pk=payment.invoice_id)
        )

        invoice.amount_paid += payment.amount
        invoice.amount_due = (
            invoice.total_amount - invoice.amount_paid
        )

        if invoice.amount_due <= Decimal("0.00"):
            invoice.amount_due = Decimal("0.00")
            invoice.status = "PAID"
        else:
            invoice.status = "PARTIALLY_PAID"

        invoice.save(
            update_fields=[
                "amount_paid",
                "amount_due",
                "status",
                "updated_at",
            ]
        )

        return payment