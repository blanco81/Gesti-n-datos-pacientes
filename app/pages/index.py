import reflex as rx
from app.state import PatientState
from app.components.datatable import patient_datatable
from app.components.modals import (
    add_patient_modal,
    view_patient_modal,
    edit_patient_modal,
    delete_patient_modal,
)


def index() -> rx.Component:
    return rx.el.div(
        rx.cond(
            PatientState.is_loading,
            rx.el.div(
                rx.spinner(size="3"),
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50",
            ),
        ),
        patient_datatable(),
        add_patient_modal(),
        view_patient_modal(),
        edit_patient_modal(),
        delete_patient_modal(),
        class_name="p-4 md:p-8 lg:p-12 bg-gray-50 min-h-screen",
        on_mount=PatientState.load_patients,
    )