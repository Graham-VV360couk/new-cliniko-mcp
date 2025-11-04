from fastmcp import FastMCP
from cliniko_client import ClinikoClient
import os
import logging

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create the FastMCP app instance
mcp = FastMCP("Cliniko MCP Server")

# Create the Cliniko client
client = ClinikoClient()

# Register all patient tools directly here
@mcp.tool("list_patients", description="List/search all Cliniko patients")
async def list_patients(q: str = "") -> dict:
    patients = await client.list_patients(q)
    return {"patients": patients}

@mcp.tool("get_patient", description="Get patient by ID")
async def get_patient(patient_id: int) -> dict:
    return await client.get_patient(patient_id)

@mcp.tool("create_patient", description="Create new patient")
async def create_patient(patient: dict) -> dict:
    return await client.create_patient(patient)

@mcp.tool("update_patient", description="Update patient details")
async def update_patient(patient_id: int, patient: dict) -> dict:
    return await client.update_patient(patient_id, patient)

@mcp.tool("delete_patient", description="Delete (archive) a patient")
async def delete_patient(patient_id: int) -> dict:
    return await client.delete_patient(patient_id)

# Register all appointment tools
@mcp.tool("list_appointments", description="List/search all Cliniko appointments")
async def list_appointments(q: str = "") -> dict:
    appointments = await client.list_appointments(q)
    return {"appointments": appointments}

@mcp.tool("get_appointment", description="Get appointment by ID")
async def get_appointment(appointment_id: int) -> dict:
    return await client.get_appointment(appointment_id)

@mcp.tool("create_appointment", description="Create new appointment")
async def create_appointment(appointment: dict) -> dict:
    return await client.create_appointment(appointment)

@mcp.tool("update_appointment", description="Update appointment details")
async def update_appointment(appointment_id: int, appointment: dict) -> dict:
    return await client.update_appointment(appointment_id, appointment)

@mcp.tool("delete_appointment", description="Delete an appointment")
async def delete_appointment(appointment_id: int) -> dict:
    return await client.delete_appointment(appointment_id)

# Register all invoice tools
@mcp.tool("list_invoices", description="List/search all Cliniko invoices")
async def list_invoices(q: str = "") -> dict:
    invoices = await client.list_invoices(q)
    return {"invoices": invoices}

@mcp.tool("get_invoice", description="Get invoice by ID")
async def get_invoice(invoice_id: int) -> dict:
    return await client.get_invoice(invoice_id)

@mcp.tool("create_invoice", description="Create new invoice")
async def create_invoice(invoice: dict) -> dict:
    return await client.create_invoice(invoice)

@mcp.tool("update_invoice", description="Update invoice details")
async def update_invoice(invoice_id: int, invoice: dict) -> dict:
    return await client.update_invoice(invoice_id, invoice)

@mcp.tool("delete_invoice", description="Delete an invoice")
async def delete_invoice(invoice_id: int) -> dict:
    return await client.delete_invoice(invoice_id)

# Register all practitioner tools
@mcp.tool("list_practitioners", description="List/search all Cliniko practitioners")
async def list_practitioners(q: str = "") -> dict:
    practitioners = await client.list_practitioners(q)
    return {"practitioners": practitioners}

@mcp.tool("get_practitioner", description="Get practitioner by ID")
async def get_practitioner(practitioner_id: int) -> dict:
    return await client.get_practitioner(practitioner_id)

@mcp.tool("create_practitioner", description="Create new practitioner")
async def create_practitioner(practitioner: dict) -> dict:
    return await client.create_practitioner(practitioner)

@mcp.tool("update_practitioner", description="Update practitioner details")
async def update_practitioner(practitioner_id: int, practitioner: dict) -> dict:
    return await client.update_practitioner(practitioner_id, practitioner)

@mcp.tool("delete_practitioner", description="Delete a practitioner")
async def delete_practitioner(practitioner_id: int) -> dict:
    return await client.delete_practitioner(practitioner_id)

# Register resources
@mcp.resource("patient://{id}", description="Get patient by ID")
async def get_patient_resource(id: int):
    return await client.get_patient(id)

@mcp.resource("patients://list", description="List all patients")
async def list_patients_resource():
    return {"patients": await client.list_patients()}

@mcp.resource("appointment://{id}", description="Get appointment by ID")
async def get_appointment_resource(id: int):
    return await client.get_appointment(id)

@mcp.resource("appointments://list", description="List all appointments")
async def list_appointments_resource():
    return {"appointments": await client.list_appointments()}


def create_app():
    """Factory function to create the app with middleware for custom routes"""
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route, Mount
    import fastmcp.server.http as http
    
    logger.info("Creating SSE app...")
    
    # Create the SSE app using FastMCP
    sse_app = http.create_sse_app(
        mcp,
        sse_path="/sse",
        message_path="/message"
    )
    
    logger.info("Creating wrapper app with custom routes...")
    
    # Define custom route handlers
    async def health_check(request):
        logger.info("Health check called")
        return JSONResponse(
            {
                "status": "healthy",
                "service": "Cliniko MCP Server",
                "transport": "sse",
                "version": "1.0"
            },
            status_code=200
        )
    
    async def root(request):
        logger.info("Root endpoint called")
        try:
            # Get tools from MCP
            tool_names = []
            if hasattr(mcp, '_tools'):
                tool_names = list(mcp._tools.keys())
        except Exception as e:
            logger.error(f"Error getting tools: {e}")
            tool_names = []
        
        return JSONResponse({
            "service": "Cliniko MCP Server",
            "version": "1.0",
            "status": "running",
            "endpoints": {
                "sse": "/sse",
                "message": "/message",
                "health": "/health",
                "root": "/"
            },
            "tools_count": len(tool_names),
            "tools": tool_names
        })
    
    # Create a new Starlette app that wraps everything
    routes = [
        Route("/health", health_check, methods=["GET"]),
        Route("/", root, methods=["GET"]),
        Mount("/", app=sse_app),  # Mount the SSE app for all other routes
    ]
    
    wrapper_app = Starlette(routes=routes)
    
    logger.info("App created successfully")
    return wrapper_app


if __name__ == "__main__":
    import uvicorn

    logger.info("🚀 Starting Cliniko MCP Server...")

    # Check registered tools
    try:
        if hasattr(mcp, '_tools'):
            tools = mcp._tools
            logger.info(f"📋 Registered tools: {len(tools)}")
            for name in tools.keys():
                logger.info(f"   ✅ {name}")
        else:
            logger.warning("No tools attribute found")
    except Exception as e:
        logger.error(f"⚠️  Error getting tools: {e}")

    # Get configuration from environment
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    transport = os.getenv("MCP_TRANSPORT", "sse").lower()

    logger.info(f"🌐 Starting MCP server on {host}:{port} using {transport} transport")

    if transport == "stdio":
        logger.info("📟 Running in stdio mode (for local AI clients)")
        mcp.run("stdio")
    elif transport in ("sse", "http"):
        logger.info("🌊 Running in HTTP/SSE mode")
        app = create_app()
        uvicorn.run(app, host=host, port=port, log_level="info")
    else:
        logger.error(f"❌ Unknown transport: {transport}. Supported: stdio, sse, http")
        exit(1)
