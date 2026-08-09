from rest_framework import serializers

from .models import (
    Invoice,
    InvoiceItem,
    Payment,
    PaymentTransaction,
    Refund,
)


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = (
            "id",
            "invoice_number",
            "created_at",
            "updated_at",
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "payment_reference",
            "invoice",
            "patient",
            "initiated_by",
            "provider",
            "method",
            "status",
            "currency",
            "amount",
            "provider_order_id",
            "provider_payment_id",
            "failure_code",
            "failure_reason",
            "paid_at",
            "metadata",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "payment_reference",
            "status",
            "provider_payment_id",
            "failure_code",
            "failure_reason",
            "paid_at",
            "created_at",
            "updated_at",
        )


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = "__all__"
        read_only_fields = tuple(
            field.name
            for field in PaymentTransaction._meta.fields
        )


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = (
            "id",
            "refund_reference",
            "payment",
            "requested_by",
            "status",
            "amount",
            "reason",
            "provider_refund_id",
            "failure_reason",
            "processed_at",
            "metadata",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "refund_reference",
            "status",
            "provider_refund_id",
            "failure_reason",
            "processed_at",
            "created_at",
            "updated_at",
        )