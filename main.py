from fastmcp import FastMCP
from cliniko_client import ClinikoClient
import os
import logging

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create the FastMCP app instance
app = FastMCP("Cliniko MCP Server")

# Create the Cliniko client
client = ClinikoClient()

# Health check handled by FastMCP's built-in server

# Register all patient tools directly here
@app.tool("list_patients", description="List/search all Cliniko patients")
async def list_patients(q: str = "") -> dict:
    patients = await client.list_patients(q)
    return {"patients": patients}

@app.tool("get_patient", description="Get patient by ID")
async def get_patient(patient_id: int) -> dict:
    return await client.get_patient(patient_id)

@app.tool("create_patient", description="Create new patient")
async def create_patient(patient: dict) -> dict:
    return await client.create_patient(patient)

@app.tool("update_patient", description="Update patient details")
async def update_patient(patient_id: int, patient: dict) -> dict:
    return await client.update_patient(patient_id, patient)

@app.tool("delete_patient", description="Delete (archive) a patient")
async def delete_patient(patient_id: int) -> dict:
    return await client.delete_patient(patient_id)

# Register all appointment tools
@app.tool("list_appointments", description="List/search all Cliniko appointments")
async def list_appointments(q: str = "") -> dict:
    appointments = await client.list_appointments(q)
    return {"appointments": appointments}

@app.tool("get_appointment", description="Get appointment by ID")
async def get_appointment(appointment_id: int) -> dict:
    return await client.get_appointment(appointment_id)

@app.tool("create_appointment", description="Create new appointment")
async def create_appointment(appointment: dict) -> dict:
    return await client.create_appointment(appointment)

@app.tool("update_appointment", description="Update appointment details")
async def update_appointment(appointment_id: int, appointment: dict) -> dict:
    return await client.update_appointment(appointment_id, appointment)

@app.tool("delete_appointment", description="Delete an appointment")
async def delete_appointment(appointment_id: int) -> dict:
    return await client.delete_appointment(appointment_id)

# Register all invoice tools
@app.tool("list_invoices", description="List/search all Cliniko invoices")
async def list_invoices(q: str = "") -> dict:
    invoices = await client.list_invoices(q)
    return {"invoices": invoices}

@app.tool("get_invoice", description="Get invoice by ID")
async def get_invoice(invoice_id: int) -> dict:
    return await client.get_invoice(invoice_id)

@app.tool("create_invoice", description="Create new invoice")
async def create_invoice(invoice: dict) -> dict:
    return await client.create_invoice(invoice)

@app.tool("update_invoice", description="Update invoice details")
async def update_invoice(invoice_id: int, invoice: dict) -> dict:
    return await client.update_invoice(invoice_id, invoice)

@app.tool("delete_invoice", description="Delete an invoice")
async def delete_invoice(invoice_id: int) -> dict:
    return await client.delete_invoice(invoice_id)

# Register all practitioner tools
@app.tool("list_practitioners", description="List/search all Cliniko practitioners")
async def list_practitioners(q: str = "") -> dict:
    practitioners = await client.list_practitioners(q)
    return {"practitioners": practitioners}

@app.tool("get_practitioner", description="Get practitioner by ID")
async def get_practitioner(practitioner_id: int) -> dict:
    return await client.get_practitioner(practitioner_id)

@app.tool("create_practitioner", description="Create new practitioner")
async def create_practitioner(practitioner: dict) -> dict:
    return await client.create_practitioner(practitioner)

@app.tool("update_practitioner", description="Update practitioner details")
async def update_practitioner(practitioner_id: int, practitioner: dict) -> dict:
    return await client.update_practitioner(practitioner_id, practitioner)

@app.tool("delete_practitioner", description="Delete a practitioner")
async def delete_practitioner(practitioner_id: int) -> dict:
    return await client.delete_practitioner(practitioner_id)

# Register resources
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

if __name__ == "__main__":
    import asyncio
    import fastmcp.server.http as http
    import uvicorn

    print("🚀 Starting Cliniko MCP Server...")

    # Check registered tools
    try:
        tools = app.get_tools()
        print(f"📋 Registered tools: {len(tools)}")
        for name, tool in tools.items():
            print(f"   ✅ {name}: {tool.description}")
    except Exception as e:
        print(f"⚠️  Error getting tools: {e}")

    print("🎯 Server ready to start...")

    # Get configuration from environment
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    transport = os.getenv("MCP_TRANSPORT", "http").lower()

    print(f"🌐 Starting MCP server on {host}:{port} using {transport} transport")

    if transport == "stdio":
        print("📟 Running in stdio mode (for local AI clients)")
        app.run("stdio")

    elif transport in ("sse", "http"):
        print("🌊 Running in HTTP/SSE mode (modern FastMCP transport)")
        app_instance = http.create_sse_app(app)
        uvicorn.run(app_instance, host=host, port=port, log_level="info")

    else:
        print(f"❌ Unknown transport: {transport}. Supported: stdio, sse, http")
        exit(1)
