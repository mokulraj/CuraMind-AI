from datetime import date

from apps.dashboard.web_views import dashboard_home
from apps.notifications.models import Notification
from apps.users.forms import ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.appointments.models import Appointment, AppointmentStatus
from apps.users.models import (
    BloodGroup,
    Gender,
    PatientProfile,
    User,
    UserRole,
)


@login_required
def home(request):
    return dashboard_home(request)


def login_page(request):

    if request.user.is_authenticated:
        return redirect("web:home")

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        print(
            "LOGIN DEBUG EMAIL =",
            repr(email),
        )

        print(
            "LOGIN DEBUG PASSWORD LENGTH =",
            len(password),
        )

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        print(
            "LOGIN DEBUG USER =",
            user,
        )

        if user is not None:

            login(
                request,
                user,
            )

            next_url = request.POST.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("web:home")

        return render(
            request,
            "auth/login.html",
            {
                "error": "Invalid email or password.",
                "next": request.POST.get(
                    "next",
                    "",
                ),
            },
        )

    return render(
        request,
        "auth/login.html",
        {
            "next": request.GET.get(
                "next",
                "",
            ),
        },
    )


def logout_view(request):

    logout(request)

    return redirect("web:login")


@login_required
def password_change_page(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST,
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user,
            )

            messages.success(
                request,
                "Your password has been changed successfully.",
            )

            return redirect(
                "web:password-change",
            )

    else:

        form = PasswordChangeForm(
            request.user,
        )

    return render(
        request,
        "auth/password_change.html",
        {
            "form": form,
        },
    )


@login_required
def patients(request):

    search_query = request.GET.get(
        "search",
        "",
    ).strip()

    patients_queryset = (
        PatientProfile.objects
        .select_related("user")
        .filter(
            user__role=UserRole.PATIENT,
        )
        .order_by(
            "user__first_name",
            "user__last_name",
        )
    )

    if search_query:

        patients_queryset = patients_queryset.filter(
            Q(user__first_name__icontains=search_query)
            | Q(user__last_name__icontains=search_query)
            | Q(user__email__icontains=search_query)
            | Q(
                medical_record_number__icontains=search_query
            )
        )

    total_patients = PatientProfile.objects.filter(
        user__role=UserRole.PATIENT,
    ).count()

    active_patients = PatientProfile.objects.filter(
        user__role=UserRole.PATIENT,
        user__is_active=True,
    ).count()

    current_month = timezone.now().date().replace(
        day=1,
    )

    new_this_month = PatientProfile.objects.filter(
        user__role=UserRole.PATIENT,
        created_at__date__gte=current_month,
    ).count()

    patient_rows = []

    for patient in patients_queryset:

        user = patient.user

        age = None

        if patient.date_of_birth:

            today = date.today()

            age = (
                today.year
                - patient.date_of_birth.year
                - (
                    (
                        today.month,
                        today.day,
                    )
                    <
                    (
                        patient.date_of_birth.month,
                        patient.date_of_birth.day,
                    )
                )
            )

        last_appointment = (
            Appointment.objects
            .filter(
                patient=patient,
                status=AppointmentStatus.COMPLETED,
            )
            .select_related("department")
            .order_by(
                "-scheduled_start",
            )
            .first()
        )

        last_visit = None
        department_name = "—"

        if last_appointment:

            last_visit = (
                last_appointment.scheduled_start
            )

            if last_appointment.department:

                department_name = (
                    last_appointment.department.name
                )

        status = (
            "Active"
            if user.is_active
            else "Inactive"
        )

        patient_rows.append(
            {
                "id": patient.id,
                "name": user.full_name,
                "email": user.email,
                "patient_id": patient.medical_record_number,
                "age": age,
                "department": department_name,
                "last_visit": last_visit,
                "status": status,
                "status_class": (
                    "active"
                    if user.is_active
                    else "inactive"
                ),
            }
        )

    return render(
        request,
        "patients.html",
        {
            "patients": patient_rows,
            "total_patients": total_patients,
            "active_patients": active_patients,
            "new_this_month": new_this_month,
            "search_query": search_query,
        },
    )


@login_required
def add_patient(request):

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            "",
        ).strip()

        last_name = request.POST.get(
            "last_name",
            "",
        ).strip()

        email = request.POST.get(
            "email",
            "",
        ).strip().lower()

        phone_number = request.POST.get(
            "phone_number",
            "",
        ).strip()

        date_of_birth = request.POST.get(
            "date_of_birth",
            "",
        ).strip()

        gender = request.POST.get(
            "gender",
            "",
        ).strip()

        blood_group = request.POST.get(
            "blood_group",
            "",
        ).strip()

        medical_record_number = request.POST.get(
            "medical_record_number",
            "",
        ).strip().upper()

        password = request.POST.get(
            "password",
            "",
        )

        confirm_password = request.POST.get(
            "confirm_password",
            "",
        )

        errors = []

        if not first_name:
            errors.append(
                "First name is required."
            )

        if not last_name:
            errors.append(
                "Last name is required."
            )

        if not email:
            errors.append(
                "Email address is required."
            )

        if not medical_record_number:
            errors.append(
                "Medical record number is required."
            )

        if not password:
            errors.append(
                "Password is required."
            )

        if password != confirm_password:
            errors.append(
                "Passwords do not match."
            )

        if len(password) < 8:
            errors.append(
                "Password must contain at least 8 characters."
            )

        if User.objects.filter(
            email__iexact=email,
        ).exists():

            errors.append(
                "A user with this email address already exists."
            )

        if PatientProfile.objects.filter(
            medical_record_number__iexact=medical_record_number,
        ).exists():

            errors.append(
                "This medical record number already exists."
            )

        if gender and gender not in dict(
            Gender.choices,
        ):

            errors.append(
                "Invalid gender selected."
            )

        if blood_group and blood_group not in dict(
            BloodGroup.choices,
        ):

            errors.append(
                "Invalid blood group selected."
            )

        if errors:

            return render(
                request,
                "patients/add_patient.html",
                {
                    "errors": errors,
                    "form_data": request.POST,
                    "gender_choices": Gender.choices,
                    "blood_group_choices": BloodGroup.choices,
                },
            )

        try:

            with transaction.atomic():

                user = User.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    role=UserRole.PATIENT,
                    is_active=True,
                )

                PatientProfile.objects.create(
                    user=user,
                    date_of_birth=(
                        date_of_birth
                        if date_of_birth
                        else None
                    ),
                    gender=gender,
                    blood_group=blood_group,
                    medical_record_number=(
                        medical_record_number
                    ),
                )

        except IntegrityError:

            return render(
                request,
                "patients/add_patient.html",
                {
                    "errors": [
                        "Unable to create patient because "
                        "some information already exists."
                    ],
                    "form_data": request.POST,
                    "gender_choices": Gender.choices,
                    "blood_group_choices": BloodGroup.choices,
                },
            )

        messages.success(
            request,
            f"Patient {first_name} {last_name} "
            "was created successfully.",
        )

        return redirect(
            "web:patients",
        )

    return render(
        request,
        "patients/add_patient.html",
        {
            "gender_choices": Gender.choices,
            "blood_group_choices": BloodGroup.choices,
        },
    )


@login_required
def appointments(request):
    return render(
        request,
        "appointments.html",
    )


@login_required
def ai_insights(request):
    return render(
        request,
        "ai_insights.html",
    )


@login_required
def medical_records(request):
    return render(
        request,
        "medical_records.html",
    )


@login_required
def imaging(request):
    return render(
        request,
        "imaging.html",
    )


@login_required
def reports(request):
    return render(
        request,
        "reports.html",
    )


@login_required
def settings_page(request):

    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            instance=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your profile has been updated successfully.",
            )

            return redirect(
                "web:settings"
            )

    else:

        form = ProfileUpdateForm(
            instance=request.user,
        )

    return render(
        request,
        "settings.html",
        {
            "form": form,
        },
    )
    
@login_required
def notifications_page(request):

    notifications = (
        Notification.objects
        .filter(user=request.user)
        .order_by("-created_at")
    )

    return render(
        request,
        "notifications/index.html",
        {
            "notifications": notifications,
        },
    )