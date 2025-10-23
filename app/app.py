import reflex as rx
from app.components.datatable import patient_datatable
from app.components.modals import (
    add_patient_modal,
    view_patient_modal,
    edit_patient_modal,
    delete_patient_modal,
)


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            patient_datatable(),
            add_patient_modal(),
            view_patient_modal(),
            edit_patient_modal(),
            delete_patient_modal(),
            class_name="p-4 md:p-6 lg:p-8",
        ),
        class_name="min-h-screen bg-gray-50 font-sans",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)