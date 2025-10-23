import reflex as rx
from app.components.datatable import patient_datatable
from app.components.modals import (
    add_patient_modal,
    view_patient_modal,
    edit_patient_modal,
    delete_patient_modal,
)


def index() -> rx.Component:
    return rx.el.div(
        patient_datatable(),
        add_patient_modal(),
        view_patient_modal(),
        edit_patient_modal(),
        delete_patient_modal(),
        class_name="p-4 md:p-8 lg:p-12 bg-gray-50 min-h-screen",
    )