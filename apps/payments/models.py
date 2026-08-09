import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel, Organization
from apps.users.models import PatientProfile, User


class PaymentProvider(models.TextChoices):
    RAZORPAY = "RAZORPAY", "Razorpay"
    STRIPE = "STRIPE", "Stripe"
    PAYPAL = "PAYPAL", "PayPal"
    MANUAL = "MANUAL", "Manual"
    OTHER = "OTHER", "Other"


class PaymentMethod(models.TextChoices):
    CARD = "CARD", "Card"
    UPI = "UPI", "UPI"
    NET_BANKING = "NET_BANKING", "Net Banking"
    WALLET = "WALLET", "Wallet"
    BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
    CASH = "CASH", "Cash"
    OTHER = "OTHER", "Other"


class PaymentStatus(models.TextChoices):
    CREATED = "CREATED", "Created"
    PENDING = "PENDING", "Pending"
    PROCESSING = "PROCESSING", "Processing"
    SUCCESS = "SUCCESS", "Successful"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"
    REFUNDED = "REFUNDED", "Refunded"
    PARTIALLY_REFUNDED = (
        "PARTIALLY_REFUNDED",
        "Partially Refunded",
    )


class InvoiceStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ISSUED = "ISSUED", "Issued"
    PARTIALLY_PAID = "PARTIALLY_PAID", "Partially Paid"
    PAID = "PAID", "Paid"
    OVERDUE = "OVERDUE", "Overdue"
    CANCELLED = "CANCELLED", "Cancelled"


class RefundStatus(models.TextChoices):
    REQUESTED = "REQUESTED", "Requested"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"
    CANCELLED = "CANCELLED", "Cancelled"


class Invoice(BaseModel):
    """
    Financial invoice issued to a patient.

    Invoice amounts are stored using Decimal for financial accuracy.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        editable=False,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    status = models.CharField(
        max_length=30,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.DRAFT,
        db_index=True,
    )

    currency = models.CharField(
        max_length=3,
        default="INR",
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    amount_due = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    issued_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    due_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "invoices"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name="invoice_org_status_idx",
            ),
            models.Index(
                fields=[
                    "patient",
                    "status",
                ],
                name="invoice_patient_status_idx",
            ),
            models.Index(
                fields=[
                    "due_at",
                    "status",
                ],
                name="invoice_due_status_idx",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = (
                f"INV-{uuid.uuid4().hex[:12].upper()}"
            )

        self.full_clean()

        super().save(*args, **kwargs)

    def clean(self):
        amounts = {
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total_amount": self.total_amount,
            "amount_paid": self.amount_paid,
            "amount_due": self.amount_due,
        }

        for name, value in amounts.items():
            if value < Decimal("0.00"):
                raise ValidationError(
                    f"{name} cannot be negative."
                )

        calculated_total = (
            self.subtotal
            + self.tax_amount
            - self.discount_amount
        )

        if self.total_amount != calculated_total:
            raise ValidationError(
                "Invoice total does not match subtotal, tax, "
                "and discount amounts."
            )

        calculated_due = (
            self.total_amount - self.amount_paid
        )

        if self.amount_due != calculated_due:
            raise ValidationError(
                "Invoice amount due does not match the "
                "total and amount paid."
            )

    def __str__(self):
        return self.invoice_number


class InvoiceItem(BaseModel):
    """
    Individual charge contained in an invoice.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name="items",
    )

    description = models.CharField(
        max_length=500,
    )

    service_code = models.CharField(
        max_length=100,
        blank=True,
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("1.00"),
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        db_table = "invoice_items"
        ordering = ["created_at"]
        indexes = [
            models.Index(
                fields=[
                    "invoice",
                    "created_at",
                ],
                name="invoice_item_date_idx",
            ),
        ]

    def clean(self):
        if self.quantity <= Decimal("0.00"):
            raise ValidationError(
                "Quantity must be greater than zero."
            )

        if self.unit_price < Decimal("0.00"):
            raise ValidationError(
                "Unit price cannot be negative."
            )

        if not 0 <= self.tax_rate <= 100:
            raise ValidationError(
                "Tax rate must be between 0 and 100."
            )

        if self.discount_amount < Decimal("0.00"):
            raise ValidationError(
                "Discount cannot be negative."
            )

        base_amount = self.quantity * self.unit_price

        tax_amount = (
            base_amount * self.tax_rate / Decimal("100")
        )

        calculated_total = (
            base_amount
            + tax_amount
            - self.discount_amount
        )

        if calculated_total < Decimal("0.00"):
            raise ValidationError(
                "Line total cannot be negative."
            )

        if self.line_total != calculated_total:
            raise ValidationError(
                "Line total does not match the item calculation."
            )

    def __str__(self):
        return self.description


class Payment(BaseModel):
    """
    Payment associated with an invoice.

    Provider-specific transaction identifiers are retained so that
    payments can be reconciled safely.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    payment_reference = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        editable=False,
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    initiated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="payments_initiated",
    )

    provider = models.CharField(
        max_length=30,
        choices=PaymentProvider.choices,
        default=PaymentProvider.RAZORPAY,
        db_index=True,
    )

    method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        db_index=True,
    )

    status = models.CharField(
        max_length=30,
        choices=PaymentStatus.choices,
        default=PaymentStatus.CREATED,
        db_index=True,
    )

    currency = models.CharField(
        max_length=3,
        default="INR",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    provider_order_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    provider_payment_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    provider_signature = models.CharField(
        max_length=512,
        blank=True,
    )

    idempotency_key = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    failure_code = models.CharField(
        max_length=100,
        blank=True,
    )

    failure_reason = models.TextField(
        blank=True,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        db_table = "payments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "invoice",
                    "status",
                ],
                name="payment_invoice_status_idx",
            ),
            models.Index(
                fields=[
                    "patient",
                    "created_at",
                ],
                name="payment_patient_date_idx",
            ),
            models.Index(
                fields=[
                    "provider",
                    "provider_payment_id",
                ],
                name="payment_provider_ref_idx",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.payment_reference:
            self.payment_reference = (
                f"PAY-{uuid.uuid4().hex[:12].upper()}"
            )

        self.full_clean()

        super().save(*args, **kwargs)

    def clean(self):
        if self.amount <= Decimal("0.00"):
            raise ValidationError(
                "Payment amount must be greater than zero."
            )

        if self.patient_id != self.invoice.patient_id:
            raise ValidationError(
                "Payment patient must match invoice patient."
            )

        if (
            self.status == PaymentStatus.SUCCESS
            and not self.provider_payment_id
            and self.provider != PaymentProvider.MANUAL
        ):
            raise ValidationError(
                "A successful provider payment must have "
                "a provider payment ID."
            )

    def __str__(self):
        return self.payment_reference


class PaymentTransactionType(models.TextChoices):
    AUTHORIZATION = "AUTHORIZATION", "Authorization"
    CAPTURE = "CAPTURE", "Capture"
    PAYMENT = "PAYMENT", "Payment"
    VOID = "VOID", "Void"
    REFUND = "REFUND", "Refund"


class PaymentTransaction(BaseModel):
    """
    Individual transaction event associated with a payment.

    This provides a financial transaction history instead of
    relying solely on the current Payment status.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    transaction_type = models.CharField(
        max_length=30,
        choices=PaymentTransactionType.choices,
        db_index=True,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=3,
        default="INR",
    )

    provider_transaction_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    success = models.BooleanField(
        default=False,
        db_index=True,
    )

    response_code = models.CharField(
        max_length=100,
        blank=True,
    )

    response_message = models.TextField(
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "payment_transactions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "payment",
                    "transaction_type",
                ],
                name="payment_transaction_type_idx",
            ),
            models.Index(
                fields=[
                    "provider_transaction_id",
                ],
                name="payment_provider_tx_idx",
            ),
        ]

    def clean(self):
        if self.amount <= Decimal("0.00"):
            raise ValidationError(
                "Transaction amount must be greater than zero."
            )

    def __str__(self):
        return (
            f"{self.payment.payment_reference} - "
            f"{self.transaction_type}"
        )


class Refund(BaseModel):
    """
    Refund request associated with a successful payment.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    refund_reference = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        editable=False,
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.PROTECT,
        related_name="refunds",
    )

    requested_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="refunds_requested",
    )

    status = models.CharField(
        max_length=20,
        choices=RefundStatus.choices,
        default=RefundStatus.REQUESTED,
        db_index=True,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    reason = models.TextField()

    provider_refund_id = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
    )

    failure_reason = models.TextField(
        blank=True,
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        db_table = "refunds"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=[
                    "payment",
                    "status",
                ],
                name="refund_payment_status_idx",
            ),
            models.Index(
                fields=[
                    "provider_refund_id",
                ],
                name="refund_provider_ref_idx",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.refund_reference:
            self.refund_reference = (
                f"REF-{uuid.uuid4().hex[:12].upper()}"
            )

        self.full_clean()

        super().save(*args, **kwargs)

    def clean(self):
        if self.amount <= Decimal("0.00"):
            raise ValidationError(
                "Refund amount must be greater than zero."
            )

        if self.payment.status not in {
            PaymentStatus.SUCCESS,
            PaymentStatus.PARTIALLY_REFUNDED,
        }:
            raise ValidationError(
                "Only successful or partially refunded payments "
                "can be refunded."
            )

        if self.amount > self.payment.amount:
            raise ValidationError(
                "Refund amount cannot exceed payment amount."
            )

        if (
            self.status == RefundStatus.COMPLETED
            and not self.provider_refund_id
            and self.payment.provider != PaymentProvider.MANUAL
        ):
            raise ValidationError(
                "Completed provider refunds must have a "
                "provider refund ID."
            )

    def __str__(self):
        return self.refund_reference