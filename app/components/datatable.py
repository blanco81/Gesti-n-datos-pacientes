import reflex as rx
from app.state import PatientState, Patient


def _table_header() -> rx.Component:
    columns = ["Name", "Sex", "Age", "Medical Record", "Actions"]
    return rx.el.thead(
        rx.el.tr(
            rx.foreach(
                columns,
                lambda col: rx.el.th(
                    col,
                    class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                ),
            ),
            class_name="bg-gray-50",
        )
    )


def _action_buttons(patient: Patient) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("eye", size=16),
            on_click=lambda: PatientState.open_modal("view", patient["id"]),
            class_name="p-2 text-gray-500 hover:text-indigo-600 hover:bg-gray-100 rounded-md transition-colors",
            title="View Details",
        ),
        rx.el.button(
            rx.icon("pencil", size=16),
            on_click=lambda: PatientState.open_modal("edit", patient["id"]),
            class_name="p-2 text-gray-500 hover:text-green-600 hover:bg-gray-100 rounded-md transition-colors",
            title="Edit Patient",
        ),
        rx.el.button(
            rx.icon("trash-2", size=16),
            on_click=lambda: PatientState.open_modal("delete", patient["id"]),
            class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-gray-100 rounded-md transition-colors",
            title="Delete Patient",
        ),
        class_name="flex items-center gap-2",
    )


def _table_row(patient: Patient) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            patient["name"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            patient["sex"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            patient["age"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            patient["medical_record"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono",
        ),
        rx.el.td(
            _action_buttons(patient),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="hover:bg-gray-50 transition-colors",
    )


def patient_datatable() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Patient Management",
                    class_name="text-xl font-semibold text-gray-900",
                ),
                rx.el.p(
                    "A list of all patients in your clinic.",
                    class_name="mt-1 text-sm text-gray-600",
                ),
                class_name="flex-1",
            ),
            rx.el.button(
                "Add New Patient",
                rx.icon("plus", class_name="ml-2", size=18),
                on_click=lambda: PatientState.open_modal("add"),
                class_name="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    _table_header(),
                    rx.el.tbody(
                        rx.foreach(PatientState.patients, _table_row),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="shadow ring-1 ring-black ring-opacity-5 rounded-lg",
        ),
    )