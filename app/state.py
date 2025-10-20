import reflex as rx
from typing import TypedDict, Optional
import uuid


class Patient(TypedDict):
    id: str
    name: str
    sex: str
    age: int
    medical_record: str


class PatientState(rx.State):
    patients: list[Patient] = [
        Patient(
            id=str(uuid.uuid4()),
            name="John Doe",
            sex="Male",
            age=45,
            medical_record="MR001",
        ),
        Patient(
            id=str(uuid.uuid4()),
            name="Jane Smith",
            sex="Female",
            age=32,
            medical_record="MR002",
        ),
        Patient(
            id=str(uuid.uuid4()),
            name="Peter Jones",
            sex="Male",
            age=58,
            medical_record="MR003",
        ),
        Patient(
            id=str(uuid.uuid4()),
            name="Mary Williams",
            sex="Female",
            age=25,
            medical_record="MR004",
        ),
        Patient(
            id=str(uuid.uuid4()),
            name="David Brown",
            sex="Male",
            age=67,
            medical_record="MR005",
        ),
    ]
    show_add_modal: bool = False
    show_view_modal: bool = False
    show_edit_modal: bool = False
    show_delete_modal: bool = False
    selected_patient: Optional[Patient] = None

    @rx.event
    def open_modal(self, modal_type: str, patient_id: Optional[str] = None):
        if patient_id:
            self.selected_patient = next(
                (p for p in self.patients if p["id"] == patient_id), None
            )
        else:
            self.selected_patient = None
        if modal_type == "add":
            self.show_add_modal = True
        elif modal_type == "view":
            self.show_view_modal = True
        elif modal_type == "edit":
            self.show_edit_modal = True
        elif modal_type == "delete":
            self.show_delete_modal = True

    @rx.event
    def close_modal(self, modal_type: str):
        if modal_type == "add":
            self.show_add_modal = False
        elif modal_type == "view":
            self.show_view_modal = False
        elif modal_type == "edit":
            self.show_edit_modal = False
        elif modal_type == "delete":
            self.show_delete_modal = False
        self.selected_patient = None

    @rx.event
    def add_patient(self, form_data: dict):
        new_patient = Patient(
            id=str(uuid.uuid4()),
            name=form_data["name"],
            sex=form_data["sex"],
            age=int(form_data["age"]),
            medical_record=form_data["medical_record"],
        )
        self.patients.append(new_patient)
        self.show_add_modal = False
        yield rx.toast.success("Patient added successfully!")

    @rx.event
    def update_patient(self, form_data: dict):
        patient_id = form_data["id"]
        for i, patient in enumerate(self.patients):
            if patient["id"] == patient_id:
                self.patients[i]["name"] = form_data["name"]
                self.patients[i]["sex"] = form_data["sex"]
                self.patients[i]["age"] = int(form_data["age"])
                self.patients[i]["medical_record"] = form_data["medical_record"]
                break
        self.show_edit_modal = False
        self.selected_patient = None
        yield rx.toast.success("Patient updated successfully!")

    @rx.event
    def delete_patient(self):
        if self.selected_patient:
            self.patients = [
                p for p in self.patients if p["id"] != self.selected_patient["id"]
            ]
            self.show_delete_modal = False
            self.selected_patient = None
            yield rx.toast.success("Patient deleted successfully!")