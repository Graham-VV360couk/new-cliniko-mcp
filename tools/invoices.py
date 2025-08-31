from cliniko_client import ClinikoClient
from main import app

client = ClinikoClient()

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
