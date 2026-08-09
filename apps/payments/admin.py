from django.contrib import admin

from .models import (
    Invoice,
    InvoiceItem,
    Payment,
    PaymentTransaction,
    Refund,
)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "organization",
        "patient",
        "status",
        "currency",
        "total_amount",
        "amount_paid",
        "amount_due",
        "due_at",
    )
    list_filter = (
        "status",
        "currency",
        "organization",
    )
    search_fields = (
        "invoice_number",
        "patient__user__email",
        "organization__name",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "id",
        "invoice_number",
        "created_at",
        "updated_at",
    )
    inlines = [
        InvoiceItemInline,
    ]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = (
        "invoice",
        "description",
        "quantity",
        "unit_price",
        "line_total",
    )
    search_fields = (
        "invoice__invoice_number",
        "description",
        "service_code",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_reference",
        "invoice",
        "patient",
        "provider",
        "method",
        "status",
        "amount",
        "paid_at",
    )
    list_filter = (
        "provider",
        "method",
        "status",
        "currency",
    )
    search_fields = (
        "payment_reference",
        "provider_order_id",
        "provider_payment_id",
        "patient__user__email",
        "invoice__invoice_number",
    )
    date_hierarchy = "created_at"
    readonly_fields = (
        "id",
        "payment_reference",
        "created_at",
        "updated_at",
    )


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "payment",
        "transaction_type",
        "amount",
        "success",
        "provider_transaction_id",
        "processed_at",
    )
    list_filter = (
        "transaction_type",
        "success",
    )
    search_fields = (
        "payment__payment_reference",
        "provider_transaction_id",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = (
        "refund_reference",
        "payment",
        "status",
        "amount",
        "provider_refund_id",
        "processed_at",
    )
    list_filter = (
        "status",
    )
    search_fields = (
        "refund_reference",
        "provider_refund_id",
        "payment__payment_reference",
    )
    readonly_fields = (
        "id",
        "refund_reference",
        "created_at",
        "updated_at",
    )