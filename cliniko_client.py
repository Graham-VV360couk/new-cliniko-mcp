import os
import httpx
import base64
from dotenv import load_dotenv

load_dotenv()

CLINIKO_API_KEY = os.getenv("CLINIKO_API_KEY")
# Try different Cliniko API endpoints based on your region
BASE_URL = "https://api.uk2.cliniko.com/v1"  # Changed from au4 to uk2

def get_auth_header():
    # Cliniko expects "Authorization: Basic <base64(key:)>"
    base = f"{CLINIKO_API_KEY}:".encode()
    b64 = base64.b64encode(base).decode()
    return {"Authorization": f"Basic {b64}"}

class ClinikoClient:
    def __init__(self):
        self.headers = get_auth_header()
        self.headers |= {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    async def list_patients(self, q=""):
        params = {"q": q} if q else {}
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/patients", headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json().get("patients", [])

    async def get_patient(self, patient_id: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/patients/{patient_id}", headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    async def create_patient(self, patient: dict):
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BASE_URL}/patients", headers=self.headers, json=patient)
            resp.raise_for_status()
            return resp.json()

    async def update_patient(self, patient_id: str, patient: dict):
        async with httpx.AsyncClient() as client:
            resp = await client.put(f"{BASE_URL}/patients/{patient_id}", headers=self.headers, json=patient)
            resp.raise_for_status()
            return resp.json()

    async def delete_patient(self, patient_id: str):
        async with httpx.AsyncClient() as client:
            resp = await client.delete(f"{BASE_URL}/patients/{patient_id}", headers=self.headers)
            resp.raise_for_status()
            return {"deleted": True}

    # Appointment methods
    async def list_appointments(self, q=""):
        params = {"q": q} if q else {}
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/appointments", headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json().get("appointments", [])

    async def get_appointment(self, appointment_id: str):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/appointments/{appointment_id}", headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    async def create_appointment(self, appointment: dict):
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BASE_URL}/appointments", headers=self.headers, json=appointment)
            resp.raise_for_status()
            return resp.json()

    async def update_appointment(self, appointment_id: str, appointment: dict):
        async with httpx.AsyncClient() as client:
            resp = await client.patch(f"{BASE_URL}/appointments/{appointment_id}", headers=self.headers, json=appointment)
            resp.raise_for_status()
            return resp.json()

    async def delete_appointment(self, appointment_id: str):
        async with httpx.AsyncClient() as client:
            resp = await client.delete(f"{BASE_URL}/appointments/{appointment_id}", headers=self.headers)
            resp.raise_for_status()
            return {"deleted": True}

    # Invoice methods
    async def list_invoices(self, q=""):
        params = {"q": q} if q else {}
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/invoices", headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json().get("invoices", [])

    async def get_invoice(self, invoice_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/invoices/{invoice_id}", headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    async def create_invoice(self, invoice: dict):
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BASE_URL}/invoices", headers=self.headers, json=invoice)
            resp.raise_for_status()
            return resp.json()

    async def update_invoice(self, invoice_id: int, invoice: dict):
        async with httpx.AsyncClient() as client:
            resp = await client.put(f"{BASE_URL}/invoices/{invoice_id}", headers=self.headers, json=invoice)
            resp.raise_for_status()
            return resp.json()

    async def delete_invoice(self, invoice_id: int):
        async with httpx.AsyncClient() as client:
            resp = await client.delete(f"{BASE_URL}/invoices/{invoice_id}", headers=self.headers)
            resp.raise_for_status()
            return {"deleted": True}

    # Practitioner methods
    async def list_practitioners(self, q=""):
        params = {"q": q} if q else {}
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/practitioners", headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json().get("practitioners", [])

    async def get_practitioner(self, practitioner_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/practitioners/{practitioner_id}", headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    async def create_practitioner(self, practitioner: dict):
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BASE_URL}/practitioners", headers=self.headers, json=practitioner)
            resp.raise_for_status()
            return resp.json()

    async def update_practitioner(self, practitioner_id: int, practitioner: dict):
        async with httpx.AsyncClient() as client:
            resp = await client.put(f"{BASE_URL}/practitioners/{practitioner_id}", headers=self.headers, json=practitioner)
            resp.raise_for_status()
            return resp.json()

    async def delete_practitioner(self, practitioner_id: int):
        async with httpx.AsyncClient() as client:
            resp = await client.delete(f"{BASE_URL}/practitioners/{practitioner_id}", headers=self.headers)
            resp.raise_for_status()
            return {"deleted": True}
