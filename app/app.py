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
            class_name="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8",
        ),
        class_name="font-['Lora'] bg-gray-50 min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)