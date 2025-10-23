import reflex as rx
from typing import TypedDict, Optional
import httpx
import asyncio
import logging

API_URL = "http://localhost:8000"


class Patient(TypedDict):
    id: str
    name: str
    sex: str
    age: int
    medical_record: str


class PatientState(rx.State):
    patients: list[Patient] = []
    show_add_modal: bool = False
    show_view_modal: bool = False
    show_edit_modal: bool = False
    show_delete_modal: bool = False
    selected_patient: Optional[Patient] = None
    is_loading: bool = False

    @rx.event(background=True)
    async def load_patients(self):
        async with self:
            self.is_loading = True
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/patients/")
                response.raise_for_status()
                async with self:
                    self.patients = response.json()
        except httpx.HTTPError as http_err:
            logging.exception(f"HTTP error occurred: {http_err}")
            yield rx.toast.error(f"HTTP error occurred: {http_err}")
        except Exception as e:
            logging.exception(f"An error occurred: {e}")
            yield rx.toast.error(f"An error occurred: {e}")
        finally:
            async with self:
                self.is_loading = False

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

    @rx.event(background=True)
    async def add_patient(self, form_data: dict):
        async with self:
            self.is_loading = True
        try:
            new_patient_data = {
                "name": form_data["name"],
                "sex": form_data["sex"],
                "age": int(form_data["age"]),
                "medical_record": form_data["medical_record"],
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/patients/", json=new_patient_data
                )
                response.raise_for_status()
            async with self:
                self.show_add_modal = False
            yield rx.toast.success("Patient added successfully!")
            yield PatientState.load_patients
        except httpx.HTTPError as http_err:
            logging.exception(f"Failed to add patient: {http_err}")
            yield rx.toast.error(f"Failed to add patient: {http_err}")
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            yield rx.toast.error(f"An unexpected error occurred: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def update_patient(self, form_data: dict):
        async with self:
            self.is_loading = True
        try:
            patient_id = form_data["id"]
            updated_data = {
                "name": form_data["name"],
                "sex": form_data["sex"],
                "age": int(form_data["age"]),
                "medical_record": form_data["medical_record"],
            }
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{API_URL}/patients/{patient_id}", json=updated_data
                )
                response.raise_for_status()
            async with self:
                self.show_edit_modal = False
                self.selected_patient = None
            yield rx.toast.success("Patient updated successfully!")
            yield PatientState.load_patients
        except httpx.HTTPError as http_err:
            logging.exception(f"Failed to update patient: {http_err}")
            yield rx.toast.error(f"Failed to update patient: {http_err}")
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            yield rx.toast.error(f"An unexpected error occurred: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event(background=True)
    async def delete_patient(self):
        async with self:
            if not self.selected_patient:
                return
            self.is_loading = True
            patient_id = self.selected_patient["id"]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{API_URL}/patients/{patient_id}")
                response.raise_for_status()
            async with self:
                self.show_delete_modal = False
                self.selected_patient = None
            yield rx.toast.success("Patient deleted successfully!")
            yield PatientState.load_patients
        except httpx.HTTPError as http_err:
            logging.exception(f"Failed to delete patient: {http_err}")
            yield rx.toast.error(f"Failed to delete patient: {http_err}")
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            yield rx.toast.error(f"An unexpected error occurred: {e}")
        finally:
            async with self:
                self.is_loading = False