from cliniko_client import ClinikoClient
from main import app

client = ClinikoClient()

@app.resource("patient://{id}", description="Get patient by ID")
async def get_patient_resource(id: int):
    return await client.get_patient(id)

@app.resource("patients://list", description="List all patients")
async def list_patients_resource():
    return {"patients": await client.list_patients()}

@app.resource("appointment://{id}", description="Get appointment by ID")
async def get_appointment_resource(id: int):
    return await client.get_appointment(id)

@app.resource("appointments://list", description="List all appointments")
async def list_appointments_resource():
    return {"appointments": await client.list_appointments()}
