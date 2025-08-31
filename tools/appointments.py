"""
Cliniko MCP Server - Appointments Module
Empirically tested and verified with actual Cliniko API responses.
"""

from cliniko_client import ClinikoClient
from main import app
from typing import Dict, Any, Optional
from datetime import datetime
import re

client = ClinikoClient()

# Verified defaults from actual working appointments
DEFAULT_PRACTITIONER_ID = "1752849161776013508"  # Yash Verma
DEFAULT_APPOINTMENT_TYPE_ID = "1752849165005627509"  # Standard appointment
DEFAULT_BUSINESS_ID = "1752849165332784051"  # Default business

def validate_iso_datetime(datetime_str: str) -> bool:
    """Validate ISO datetime format: YYYY-MM-DDTHH:MM:SSZ"""
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    return bool(re.match(pattern, datetime_str))

def validate_id_format(id_str: str) -> bool:
    """Validate ID is a string of digits"""
    return isinstance(id_str, str) and id_str.isdigit() and len(id_str) > 10

@app.tool("list_appointments", 
         description="List all Cliniko appointments. Use empty string for q to get all appointments.")
async def list_appointments(q: str = "") -> dict:
    """
    List appointments with optional search query.
    
    Args:
        q: Search query (empty string returns all appointments)
    
    Returns:
        dict: {"appointments": [array of appointment objects]}
    
    Note: Search by patient name may not work in all Cliniko instances.
    Use empty string to get all appointments and filter client-side.
    """
    try:
        appointments = await client.list_appointments(q)
        return {"appointments": appointments}
    except Exception as e:
        return {"error": f"Failed to list appointments: {str(e)}", "appointments": []}

@app.tool("get_appointment", 
         description="Get a specific appointment by its ID (as string)")
async def get_appointment(appointment_id: str) -> dict:
    """
    Retrieve a specific appointment.
    
    Args:
        appointment_id: Appointment ID as string (e.g., "1764041108192502241")
    
    Returns:
        dict: Complete appointment object or error
    """
    if not validate_id_format(appointment_id):
        return {
            "error": "Invalid appointment_id format. Must be a string of digits.",
            "example": "1764041108192502241"
        }
    
    try:
        return await client.get_appointment(appointment_id)
    except Exception as e:
        return {"error": f"Failed to get appointment: {str(e)}"}

@app.tool("create_appointment", 
         description="""Create new appointment in Cliniko.

EMPIRICALLY VERIFIED FIELD NAMES (tested successfully):
✅ patient_id: String ID of patient (required)
✅ practitioner_id: String ID of practitioner (required) 
✅ appointment_type_id: String ID of appointment type (required)
✅ business_id: String ID of business/clinic (required)
✅ appointment_start: ISO datetime "YYYY-MM-DDTHH:MM:SSZ" (required)
✅ appointment_end: ISO datetime "YYYY-MM-DDTHH:MM:SSZ" (required)
✅ notes: String notes (optional)

ALTERNATIVE FIELD NAMES (also tested and work):
✅ starts_at: ISO datetime (instead of appointment_start)
✅ ends_at: ISO datetime (instead of appointment_end)

WORKING EXAMPLE (copy exactly):
{
  "patient_id": "1764028746571981724",
  "practitioner_id": "1752849161776013508",
  "appointment_type_id": "1752849165005627509",
  "business_id": "1752849165332784051",
  "appointment_start": "2025-09-05T10:00:00Z",
  "appointment_end": "2025-09-05T11:00:00Z",
  "notes": "Appointment created via MCP"
}

DEFAULTS AVAILABLE:
- practitioner_id: "1752849161776013508" (Yash Verma)
- appointment_type_id: "1752849165005627509" (Standard)
- business_id: "1752849165332784051" (Default clinic)""")
async def create_appointment(appointment: dict) -> dict:
    """
    Create a new appointment using empirically verified field names.
    
    Args:
        appointment: Dict with appointment data
        
    Required fields:
        - patient_id (string)
        - practitioner_id (string) 
        - appointment_type_id (string)
        - business_id (string)
        - appointment_start OR starts_at (ISO datetime string)
        - appointment_end OR ends_at (ISO datetime string)
        
    Returns:
        dict: Created appointment object with ID, or detailed error
    """
    
    # Check for required fields (supporting both naming conventions)
    required_base_fields = ["patient_id", "practitioner_id", "appointment_type_id", "business_id"]
    missing_base = [f for f in required_base_fields if f not in appointment]
    
    # Check for time fields (either convention)
    has_appointment_time = "appointment_start" in appointment and "appointment_end" in appointment
    has_starts_ends_time = "starts_at" in appointment and "ends_at" in appointment
    
    if missing_base:
        return {
            "error": f"Missing required fields: {', '.join(missing_base)}",
            "required_fields": required_base_fields + ["appointment_start", "appointment_end"],
            "working_example": {
                "patient_id": "1764028746571981724",
                "practitioner_id": DEFAULT_PRACTITIONER_ID,
                "appointment_type_id": DEFAULT_APPOINTMENT_TYPE_ID,
                "business_id": DEFAULT_BUSINESS_ID,
                "appointment_start": "2025-09-05T10:00:00Z",
                "appointment_end": "2025-09-05T11:00:00Z",
                "notes": "Optional notes"
            },
            "defaults": {
                "practitioner_id": DEFAULT_PRACTITIONER_ID,
                "appointment_type_id": DEFAULT_APPOINTMENT_TYPE_ID,
                "business_id": DEFAULT_BUSINESS_ID
            }
        }
    
    if not has_appointment_time and not has_starts_ends_time:
        return {
            "error": "Missing time fields. Provide either (appointment_start + appointment_end) OR (starts_at + ends_at)",
            "option1": "appointment_start and appointment_end",
            "option2": "starts_at and ends_at",
            "format": "ISO datetime: YYYY-MM-DDTHH:MM:SSZ",
            "example": "2025-09-05T10:00:00Z"
        }
    
    # Validate ID formats
    for field in ["patient_id", "practitioner_id", "appointment_type_id", "business_id"]:
        if field in appointment and not validate_id_format(appointment[field]):
            return {
                "error": f"Invalid {field} format. Must be string of digits.",
                "received": appointment[field],
                "example": "1764028746571981724"
            }
    
    # Validate datetime formats
    datetime_fields = []
    if has_appointment_time:
        datetime_fields = ["appointment_start", "appointment_end"]
    elif has_starts_ends_time:
        datetime_fields = ["starts_at", "ends_at"]
    
    for field in datetime_fields:
        if not validate_iso_datetime(appointment[field]):
            return {
                "error": f"Invalid {field} format. Must be ISO datetime with Z suffix.",
                "received": appointment[field],
                "required_format": "YYYY-MM-DDTHH:MM:SSZ",
                "example": "2025-09-05T10:00:00Z"
            }
    
    try:
        result = await client.create_appointment(appointment)
        if "id" in result:
            return {
                "success": True,
                "appointment": result,
                "appointment_id": result["id"],
                "patient_name": result.get("patient_name", "Unknown"),
                "start_time": result.get("starts_at") or result.get("appointment_start"),
                "end_time": result.get("ends_at") or result.get("appointment_end")
            }
        return result
    except Exception as e:
        return {
            "error": f"API call failed: {str(e)}",
            "troubleshooting": "Check that all IDs exist in your Cliniko instance and datetime is in future"
        }

@app.tool("update_appointment", 
         description="""Update existing appointment in Cliniko.

EMPIRICALLY VERIFIED UPDATE FIELD NAMES (different from create):
✅ starts_at: ISO datetime "YYYY-MM-DDTHH:MM:SSZ" (for appointment start time)
✅ ends_at: ISO datetime "YYYY-MM-DDTHH:MM:SSZ" (for appointment end time)
✅ notes: String notes (optional)

NOTE: Updates use different field names than create!
- CREATE uses: appointment_start/appointment_end
- UPDATE uses: starts_at/ends_at

WORKING UPDATE EXAMPLE:
{
  "starts_at": "2025-09-07T14:00:00Z",
  "ends_at": "2025-09-07T15:00:00Z", 
  "notes": "Updated appointment time"
}""")
async def update_appointment(appointment_id: str, appointment: dict) -> dict:
    """
    Update an existing appointment using PATCH method and correct field names.
    
    Args:
        appointment_id: Appointment ID as string
        appointment: Dict with update fields (starts_at, ends_at, notes)
    
    Returns:
        dict: Updated appointment object or error
    """
    if not validate_id_format(appointment_id):
        return {
            "error": "Invalid appointment_id format",
            "example": "1764041108192502241"
        }
    
    # Validate datetime formats if provided
    validation_errors = []
    for field in ["starts_at", "ends_at"]:
        if field in appointment and not validate_iso_datetime(appointment[field]):
            validation_errors.append(f"Invalid {field} format. Must be ISO datetime with Z suffix.")
    
    if validation_errors:
        return {
            "error": "Validation failed",
            "validation_errors": validation_errors,
            "required_format": "YYYY-MM-DDTHH:MM:SSZ",
            "example": "2025-09-07T14:00:00Z",
            "correct_update_example": {
                "starts_at": "2025-09-07T14:00:00Z",
                "ends_at": "2025-09-07T15:00:00Z",
                "notes": "Updated appointment time"
            }
        }
    
    try:
        result = await client.update_appointment(appointment_id, appointment)
        if "id" in result:
            return {
                "success": True,
                "appointment": result,
                "appointment_id": result["id"],
                "patient_name": result.get("patient_name", "Unknown"),
                "updated_start_time": result.get("starts_at"),
                "updated_end_time": result.get("ends_at"),
                "updated_at": result.get("updated_at")
            }
        return result
    except Exception as e:
        return {
            "error": f"Failed to update appointment: {str(e)}",
            "troubleshooting": "Ensure appointment ID exists and you have permission to update it"
        }

@app.tool("delete_appointment", 
         description="Delete (cancel) an appointment by ID")
async def delete_appointment(appointment_id: str) -> dict:
    """
    Delete/cancel an appointment.
    
    Args:
        appointment_id: Appointment ID as string
    
    Returns:
        dict: Deletion confirmation or error
    """
    if not validate_id_format(appointment_id):
        return {
            "error": "Invalid appointment_id format",
            "example": "1764041108192502241"
        }
    
    try:
        result = await client.delete_appointment(appointment_id)
        return {
            "success": True,
            "message": f"Appointment {appointment_id} deleted successfully",
            "result": result
        }
    except Exception as e:
        return {"error": f"Failed to delete appointment: {str(e)}"}
