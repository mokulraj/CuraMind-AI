from django.urls import path

from .views import (
    home,
    login_page,
    notifications_page,
    password_change_page,
)
from .views import (
    home,
    appointments,
    patients,
    add_patient,
    ai_insights,
    medical_records,
    imaging,
    reports,
    settings_page,
    login_page,
    password_change_page,
    logout_view,
)


app_name = "web"


urlpatterns = [

    # Dashboard
    path(
        "",
        home,
        name="home",
    ),

    # Patients
    path(
        "patients/",
        patients,
        name="patients",
    ),

    path(
        "patients/add/",
        add_patient,
        name="add-patient",
    ),

    # Appointments
    path(
        "appointments/",
        appointments,
        name="appointments",
    ),

    # AI Insights
    path(
        "ai-insights/",
        ai_insights,
        name="ai-insights",
    ),

    # Medical Records
    path(
        "medical-records/",
        medical_records,
        name="medical-records",
    ),

    # Imaging
    path(
        "imaging/",
        imaging,
        name="imaging",
    ),
    
    path(
    "notifications/",
    notifications_page,
    name="notifications",
),

    # Reports
    path(
        "reports/",
        reports,
        name="reports",
    ),

    # Settings
    path(
        "settings/",
        settings_page,
        name="settings",
    ),

    # Authentication
    path(
        "login/",
        login_page,
        name="login",
    ),

    path(
        "logout/",
        logout_view,
        name="logout",
    ),

    path(
        "password/change/",
        password_change_page,
        name="password-change",
    ),
]