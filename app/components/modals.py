import reflex as rx
from app.state import PatientState, Patient


def _modal_overlay() -> rx.Component:
    return rx.el.div(class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40")


def _modal_content_wrapper(content: rx.Component) -> rx.Component:
    return rx.el.div(
        content,
        class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-6 md:p-8 w-full max-w-md z-50",
    )


def _modal_header(title: str) -> rx.Component:
    return rx.el.h2(title, class_name="text-2xl font-bold text-gray-800 mb-6")


def _form_field(
    label: str,
    name: str,
    type: str,
    default_value: rx.Var | str = "",
    placeholder: str = "",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            name=name,
            type=type,
            default_value=default_value,
            placeholder=placeholder,
            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors",
        ),
        class_name="mb-4",
    )


def _sex_select(default_value: rx.Var | str) -> rx.Component:
    return rx.el.div(
        rx.el.label("Sex", class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.select(
            rx.el.option("Male", value="Male"),
            rx.el.option("Female", value="Female"),
            name="sex",
            default_value=default_value,
            class_name="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors bg-white",
        ),
        class_name="mb-4",
    )


def _modal_footer(cancel_event, submit_text: str) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Cancel",
            on_click=cancel_event,
            type="button",
            class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors font-medium",
        ),
        rx.el.button(
            submit_text,
            type="submit",
            class_name="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium",
        ),
        class_name="flex justify-end gap-4 mt-6",
    )


def add_patient_modal() -> rx.Component:
    return rx.cond(
        PatientState.show_add_modal,
        rx.el.div(
            _modal_overlay(),
            _modal_content_wrapper(
                rx.el.form(
                    _modal_header("Add New Patient"),
                    _form_field(
                        "Full Name", "name", "text", placeholder="e.g. John Doe"
                    ),
                    _sex_select("Male"),
                    _form_field("Age", "age", "number", placeholder="e.g. 45"),
                    _form_field(
                        "Medical Record No.",
                        "medical_record",
                        "text",
                        placeholder="e.g. MR001",
                    ),
                    _modal_footer(
                        lambda: PatientState.close_modal("add"), "Add Patient"
                    ),
                    on_submit=PatientState.add_patient,
                    reset_on_submit=True,
                )
            ),
        ),
    )


def view_patient_modal() -> rx.Component:
    return rx.cond(
        PatientState.show_view_modal,
        rx.el.div(
            _modal_overlay(),
            rx.cond(
                PatientState.selected_patient,
                _modal_content_wrapper(
                    rx.el.div(
                        _modal_header("Patient Details"),
                        rx.el.div(
                            rx.el.p(
                                rx.el.span(
                                    "Name: ", class_name="font-semibold text-gray-700"
                                ),
                                PatientState.selected_patient["name"],
                            ),
                            rx.el.p(
                                rx.el.span(
                                    "Sex: ", class_name="font-semibold text-gray-700"
                                ),
                                PatientState.selected_patient["sex"],
                            ),
                            rx.el.p(
                                rx.el.span(
                                    "Age: ", class_name="font-semibold text-gray-700"
                                ),
                                PatientState.selected_patient["age"],
                            ),
                            rx.el.p(
                                rx.el.span(
                                    "Medical Record: ",
                                    class_name="font-semibold text-gray-700",
                                ),
                                PatientState.selected_patient["medical_record"],
                            ),
                            class_name="space-y-3 text-gray-800",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Close",
                                on_click=lambda: PatientState.close_modal("view"),
                                class_name="mt-6 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium",
                            ),
                            class_name="flex justify-end",
                        ),
                    )
                ),
            ),
        ),
    )


def edit_patient_modal() -> rx.Component:
    return rx.cond(
        PatientState.show_edit_modal,
        rx.el.div(
            _modal_overlay(),
            rx.cond(
                PatientState.selected_patient,
                _modal_content_wrapper(
                    rx.el.form(
                        _modal_header("Edit Patient"),
                        rx.el.input(
                            type="hidden",
                            name="id",
                            default_value=PatientState.selected_patient["id"],
                        ),
                        _form_field(
                            "Full Name",
                            "name",
                            "text",
                            default_value=PatientState.selected_patient["name"],
                        ),
                        _sex_select(PatientState.selected_patient["sex"]),
                        _form_field(
                            "Age",
                            "age",
                            "number",
                            default_value=PatientState.selected_patient[
                                "age"
                            ].to_string(),
                        ),
                        _form_field(
                            "Medical Record No.",
                            "medical_record",
                            "text",
                            default_value=PatientState.selected_patient[
                                "medical_record"
                            ],
                        ),
                        _modal_footer(
                            lambda: PatientState.close_modal("edit"), "Save Changes"
                        ),
                        on_submit=PatientState.update_patient,
                        reset_on_submit=True,
                    )
                ),
            ),
        ),
    )


def delete_patient_modal() -> rx.Component:
    return rx.cond(
        PatientState.show_delete_modal,
        rx.el.div(
            _modal_overlay(),
            rx.cond(
                PatientState.selected_patient,
                _modal_content_wrapper(
                    rx.el.div(
                        _modal_header("Confirm Deletion"),
                        rx.el.p(
                            "Are you sure you want to delete the record for ",
                            rx.el.strong(PatientState.selected_patient["name"]),
                            "? This action cannot be undone.",
                            class_name="text-gray-600",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Cancel",
                                on_click=lambda: PatientState.close_modal("delete"),
                                class_name="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors font-medium",
                            ),
                            rx.el.button(
                                "Delete",
                                on_click=PatientState.delete_patient,
                                class_name="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium",
                            ),
                            class_name="flex justify-end gap-4 mt-6",
                        ),
                    )
                ),
            ),
        ),
    )