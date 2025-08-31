from cliniko_client import ClinikoClient
from main import app

client = ClinikoClient()

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
