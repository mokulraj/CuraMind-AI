from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.users.models import UserRole


@login_required
def role_dashboard(request):
    """
    Render the dashboard designed for the authenticated user's role.
    """

    role_config = {
        UserRole.PATIENT: {
            "template": "dashboard/roles/patient.html",
            "title": "Patient Dashboard",
            "description": (
                "Manage your appointments, medical records, "
                "reports and healthcare activity."
            ),
            "eyebrow": "PATIENT",
        },

        UserRole.DOCTOR: {
            "template": "dashboard/roles/doctor.html",
            "title": "Doctor Dashboard",
            "description": (
                "Manage patients, appointments, clinical records "
                "and AI insights."
            ),
            "eyebrow": "DOCTOR",
        },

        UserRole.NURSE: {
            "template": "dashboard/roles/nurse.html",
            "title": "Nurse Dashboard",
            "description": (
                "Manage patient care, vitals, tasks "
                "and clinical activities."
            ),
            "eyebrow": "NURSE",
        },

        UserRole.ADMIN: {
            "template": "dashboard/roles/admin.html",
            "title": "Administrator Dashboard",
            "description": (
                "Manage users, healthcare operations, "
                "analytics and system settings."
            ),
            "eyebrow": "ADMINISTRATION",
        },

        UserRole.STAFF: {
            "template": "dashboard/roles/staff.html",
            "title": "Staff Dashboard",
            "description": (
                "Manage appointments, patients "
                "and daily healthcare operations."
            ),
            "eyebrow": "STAFF",
        },

        UserRole.RADIOLOGIST: {
            "template": "dashboard/roles/radiologist.html",
            "title": "Radiologist Dashboard",
            "description": (
                "Review imaging studies, AI-assisted findings "
                "and radiology reports."
            ),
            "eyebrow": "RADIOLOGY",
        },

        UserRole.LAB_TECHNICIAN: {
            "template": "dashboard/roles/lab_technician.html",
            "title": "Lab Technician Dashboard",
            "description": (
                "Manage laboratory orders, samples, "
                "results and reports."
            ),
            "eyebrow": "LABORATORY",
        },
    }

    config = role_config.get(
        request.user.role,
    )

    if config is None:
        return render(
            request,
            "dashboard/roles/default.html",
            {
                "current_role": request.user.role,
            },
        )

    return render(
        request,
        config["template"],
        {
            "current_role": request.user.role,
            "dashboard_title": config["title"],
            "dashboard_description": config["description"],
            "role_eyebrow": config["eyebrow"],
        },
    )