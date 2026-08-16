from datetime import timedelta

from django import forms
from django.utils import timezone

from apps.appointments.models import (
    AppointmentType,
    ConsultationMode,
)
from apps.core.models import (
    Department,
    Organization,
)
from apps.users.models import DoctorProfile


class AppointmentForm(forms.Form):
    """
    Form used by patients to schedule appointments.
    """

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.none(),
        empty_label="Select healthcare organization",
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        empty_label="Select department",
    )

    doctor = forms.ModelChoiceField(
        queryset=DoctorProfile.objects.none(),
        empty_label="Select doctor",
    )

    appointment_type = forms.ChoiceField(
        choices=AppointmentType.choices,
    )

    consultation_mode = forms.ChoiceField(
        choices=ConsultationMode.choices,
    )

    scheduled_start = forms.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M",
        ],
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={
                "type": "datetime-local",
            },
        ),
    )

    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": (
                    "Briefly describe the reason "
                    "for your appointment."
                ),
            }
        ),
    )

    symptoms = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": (
                    "Describe any symptoms you "
                    "are currently experiencing."
                ),
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[
            "organization"
        ].queryset = (
            Organization.objects
            .filter(
                is_active=True,
                is_deleted=False,
            )
            .order_by("name")
        )

        self.fields[
            "department"
        ].queryset = (
            Department.objects
            .filter(
                is_active=True,
                is_deleted=False,
            )
            .select_related("organization")
            .order_by(
                "organization__name",
                "name",
            )
        )

        self.fields[
            "doctor"
        ].queryset = (
            DoctorProfile.objects
            .filter(
                is_verified=True,
                user__is_active=True,
            )
            .select_related("user")
            .order_by(
                "user__first_name",
                "user__last_name",
            )
        )

    def clean_scheduled_start(self):
        scheduled_start = (
            self.cleaned_data["scheduled_start"]
        )

        if timezone.is_naive(scheduled_start):
            scheduled_start = timezone.make_aware(
                scheduled_start,
                timezone.get_current_timezone(),
            )

        if scheduled_start <= timezone.now():
            raise forms.ValidationError(
                "Please select a future date and time."
            )

        return scheduled_start

    def clean(self):
        cleaned_data = super().clean()

        organization = cleaned_data.get(
            "organization"
        )

        department = cleaned_data.get(
            "department"
        )

        if (
            organization
            and department
            and department.organization_id
            != organization.id
        ):
            self.add_error(
                "department",
                "The selected department does not "
                "belong to the selected organization.",
            )

        return cleaned_data

    def get_scheduled_end(self):
        """
        CuraMind currently uses a 30-minute
        appointment duration.
        """

        return (
            self.cleaned_data["scheduled_start"]
            + timedelta(minutes=30)
        )