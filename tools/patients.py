"""
Cliniko MCP Server - Patients Module
Empirically tested and verified with actual Cliniko API responses.
"""

from cliniko_client import ClinikoClient
from main import app
from typing import Dict, Any, Optional
import re

client = ClinikoClient()

def validate_id_format(id_str: str) -> bool:
    """Validate ID is a string of digits"""
    return isinstance(id_str, str) and id_str.isdigit() and len(id_str) > 10

def validate_date_format(date_str: str) -> bool:
    """Validate date format: YYYY-MM-DD"""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_str))

def validate_email_format(email: str) -> bool:
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@app.tool("list_patients", 
         description="List all Cliniko patients. Use empty string for q to get all patients.")
async def list_patients(q: str = "") -> dict:
    """
    List patients with optional search query.
    
    Args:
        q: Search query (empty string returns all patients)
    
    Returns:
        dict: {"patients": [array of patient objects]}
    
    Note: Search by patient name may not work in all Cliniko instances.
    Use empty string to get all patients and filter client-side.
    """
    try:
        patients = await client.list_patients(q)
        return {"patients": patients}
    except Exception as e:
        return {"error": f"Failed to list patients: {str(e)}", "patients": []}

@app.tool("get_patient", 
         description="Get a specific patient by their ID (as string)")
async def get_patient(patient_id: str) -> dict:
    """
    Retrieve a specific patient.
    
    Args:
        patient_id: Patient ID as string (e.g., "1764041171115451305")
    
    Returns:
        dict: Complete patient object or error
    """
    if not validate_id_format(patient_id):
        return {
            "error": "Invalid patient_id format. Must be a string of digits.",
            "example": "1764041171115451305"
        }
    
    try:
        return await client.get_patient(patient_id)
    except Exception as e:
        return {"error": f"Failed to get patient: {str(e)}"}

@app.tool("create_patient", 
         description="""Create new patient in Cliniko.

EMPIRICALLY VERIFIED FIELDS (tested successfully):
✅ first_name: Patient's first name (REQUIRED, string)
✅ last_name: Patient's last name (REQUIRED, string)
✅ email: Email address (optional, string)
✅ date_of_birth: Date in YYYY-MM-DD format (optional, string)
✅ title: Title like "Mr", "Mrs", "Dr" (optional, string)
✅ gender_identity: Gender identity (optional, string)
✅ sex: Sex assigned at birth (optional, string)
✅ address_1: Primary address line (optional, string)
✅ address_2: Secondary address line (optional, string)
✅ address_3: Third address line (optional, string)
✅ city: City (optional, string)
✅ country: Country name (optional, string)
✅ post_code: Postal/ZIP code (optional, string)
✅ notes: Patient notes (optional, string)
✅ occupation: Patient's occupation (optional, string)
✅ emergency_contact: Emergency contact info (optional, string)

WORKING EXAMPLE (tested successfully):
{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@email.com",
  "date_of_birth": "1985-03-15",
  "title": "Mr",
  "sex": "Male",
  "address_1": "123 Main Street",
  "city": "London",
  "country": "United Kingdom",
  "post_code": "SW1A 1AA",
  "occupation": "Software Engineer"
}

MINIMAL EXAMPLE:
{
  "first_name": "John",
  "last_name": "Smith"
}""")
async def create_patient(patient: dict) -> dict:
    """
    Create a new patient using empirically verified field names.
    
    Args:
        patient: Dict with patient data
        
    Required fields:
        - first_name (string)
        - last_name (string)
        
    Optional fields:
        - email, date_of_birth, title, sex, gender_identity
        - address_1, address_2, address_3, city, country, post_code
        - notes, occupation, emergency_contact
        
    Returns:
        dict: Created patient object with ID, or detailed error
    """
    
    # Validate required fields
    required_fields = ["first_name", "last_name"]
    missing_fields = [f for f in required_fields if f not in patient or not patient[f]]
    
    if missing_fields:
        return {
            "error": f"Missing required fields: {', '.join(missing_fields)}",
            "required_fields": required_fields,
            "minimal_example": {
                "first_name": "John",
                "last_name": "Smith"
            },
            "complete_example": {
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@email.com",
                "date_of_birth": "1985-03-15",
                "title": "Mr",
                "sex": "Male",
                "address_1": "123 Main Street",
                "city": "London",
                "country": "United Kingdom",
                "post_code": "SW1A 1AA",
                "occupation": "Software Engineer"
            }
        }
    
    # Validate optional fields if provided
    validation_errors = []
    
    if "email" in patient and patient["email"]:
        if not validate_email_format(patient["email"]):
            validation_errors.append("Invalid email format")
    
    if "date_of_birth" in patient and patient["date_of_birth"]:
        if not validate_date_format(patient["date_of_birth"]):
            validation_errors.append("Invalid date_of_birth format. Use YYYY-MM-DD")
    
    # Check for empty required fields
    for field in required_fields:
        if not patient[field].strip():
            validation_errors.append(f"{field} cannot be empty")
    
    if validation_errors:
        return {
            "error": "Validation failed",
            "validation_errors": validation_errors,
            "email_format": "user@example.com",
            "date_format": "1985-03-15 (YYYY-MM-DD)"
        }
    
    try:
        result = await client.create_patient(patient)
        if "id" in result:
            return {
                "success": True,
                "patient": result,
                "patient_id": result["id"],
                "patient_name": f"{result.get('first_name', '')} {result.get('last_name', '')}".strip(),
                "email": result.get("email"),
                "label": result.get("label")
            }
        return result
    except Exception as e:
        return {
            "error": f"API call failed: {str(e)}",
            "troubleshooting": "Check that email is unique and date format is correct"
        }

@app.tool("update_patient", 
         description="Update existing patient. Use same field names as create_patient.")
async def update_patient(patient_id: str, patient: dict) -> dict:
    """
    Update an existing patient.
    
    Args:
        patient_id: Patient ID as string
        patient: Dict with fields to update (same format as create)
    
    Returns:
        dict: Updated patient object or error
    """
    if not validate_id_format(patient_id):
        return {
            "error": "Invalid patient_id format",
            "example": "1764041171115451305"
        }
    
    # Validate fields if provided
    validation_errors = []
    
    if "email" in patient and patient["email"]:
        if not validate_email_format(patient["email"]):
            validation_errors.append("Invalid email format")
    
    if "date_of_birth" in patient and patient["date_of_birth"]:
        if not validate_date_format(patient["date_of_birth"]):
            validation_errors.append("Invalid date_of_birth format. Use YYYY-MM-DD")
    
    if validation_errors:
        return {
            "error": "Validation failed",
            "validation_errors": validation_errors
        }
    
    try:
        return await client.update_patient(patient_id, patient)
    except Exception as e:
        return {"error": f"Failed to update patient: {str(e)}"}

@app.tool("delete_patient", 
         description="Delete (archive) a patient by ID")
async def delete_patient(patient_id: str) -> dict:
    """
    Archive/delete a patient.
    
    Args:
        patient_id: Patient ID as string
    
    Returns:
        dict: Deletion confirmation or error
    """
    if not validate_id_format(patient_id):
        return {
            "error": "Invalid patient_id format",
            "example": "1764041171115451305"
        }
    
    try:
        result = await client.delete_patient(patient_id)
        return {
            "success": True,
            "message": f"Patient {patient_id} archived successfully",
            "result": result
        }
    except Exception as e:
        return {"error": f"Failed to delete patient: {str(e)}"}
