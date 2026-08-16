from django.urls import path

from .views import (
    home,
    appointments,
    new_appointment,
    cancel_appointment,
    confirm_appointment,
    start_appointment,
    complete_appointment,
    patients,
    add_patient,
    ai_insights,
    medical_records,
    medical_record_detail,
    reports,
    settings_page,
    login_page,
    password_change_page,
    logout_view,
    notifications_page,
    create_clinical_note,
    sign_clinical_note,
    update_clinical_encounter,
    complete_clinical_encounter,
    cancel_clinical_encounter,
)


app_name = "web"


urlpatterns = [

    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    path(
        "",
        home,
        name="home",
    ),

    # --------------------------------------------------
    # PATIENTS
    # --------------------------------------------------

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

    # --------------------------------------------------
    # APPOINTMENTS
    # --------------------------------------------------

    path(
        "appointments/",
        appointments,
        name="appointments",
    ),

    path(
        "appointments/new/",
        new_appointment,
        name="appointment-new",
    ),

    path(
        "appointments/<uuid:appointment_id>/cancel/",
        cancel_appointment,
        name="appointment-cancel",
    ),

    path(
        "appointments/<uuid:appointment_id>/confirm/",
        confirm_appointment,
        name="appointment-confirm",
    ),

    path(
        "appointments/<uuid:appointment_id>/start/",
        start_appointment,
        name="appointment-start",
    ),

    path(
        "appointments/<uuid:appointment_id>/complete/",
        complete_appointment,
        name="appointment-complete",
    ),
    
        # --------------------------------------------------
    # CLINICAL NOTES
    # --------------------------------------------------

    path(
        "medical-records/<uuid:record_id>/encounters/<uuid:encounter_id>/notes/create/",
        create_clinical_note,
        name="clinical-note-create",
    ),

    path(
        "medical-records/<uuid:record_id>/notes/<uuid:note_id>/sign/",
        sign_clinical_note,
        name="clinical-note-sign",
    ),

    # --------------------------------------------------
    
    # --------------------------------------------------
# CLINICAL ENCOUNTERS
# --------------------------------------------------

path(
    "medical-records/<uuid:record_id>/encounters/<uuid:encounter_id>/update/",
    update_clinical_encounter,
    name="clinical-encounter-update",
),

path(
    "medical-records/<uuid:record_id>/encounters/<uuid:encounter_id>/complete/",
    complete_clinical_encounter,
    name="clinical-encounter-complete",
),

path(
    "medical-records/<uuid:record_id>/encounters/<uuid:encounter_id>/cancel/",
    cancel_clinical_encounter,
    name="clinical-encounter-cancel",
),


    # AI INSIGHTS
    # --------------------------------------------------

    path(
        "ai-insights/",
        ai_insights,
        name="ai-insights",
    ),

    # --------------------------------------------------
    # MEDICAL RECORDS
    # --------------------------------------------------

    path(
        "medical-records/",
        medical_records,
        name="medical-records",
    ),

    path(
        "medical-records/<uuid:record_id>/",
        medical_record_detail,
        name="medical-record-detail",
    ),

    # --------------------------------------------------
    # NOTIFICATIONS
    # --------------------------------------------------

    path(
        "notifications/",
        notifications_page,
        name="notifications",
    ),

    # --------------------------------------------------
    # REPORTS
    # --------------------------------------------------

    path(
        "reports/",
        reports,
        name="reports",
    ),

    # --------------------------------------------------
    # SETTINGS
    # --------------------------------------------------

    path(
        "settings/",
        settings_page,
        name="settings",
    ),

    # --------------------------------------------------
    # AUTHENTICATION
    # --------------------------------------------------

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