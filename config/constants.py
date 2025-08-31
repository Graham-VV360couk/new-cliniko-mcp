# Cliniko MCP Server Constants
# This file contains common IDs and configurations for reliable tool usage

# Default Business Configuration
DEFAULT_BUSINESS_ID = "1752849165332784051"  # Default business for appointments

# Default Appointment Type
DEFAULT_APPOINTMENT_TYPE_ID = "1752849165005627509"  # Standard appointment type

# Default Practitioner (Yash Verma)
DEFAULT_PRACTITIONER_ID = "1752849161776013508"

# Common Time Zones
DEFAULT_TIMEZONE = "UTC"

# Appointment Duration Templates (in hours)
APPOINTMENT_DURATIONS = {
    "consultation": 1,      # 1 hour
    "follow_up": 0.5,      # 30 minutes  
    "checkup": 1,          # 1 hour
    "procedure": 2,        # 2 hours
    "short": 0.25,         # 15 minutes
}

# Date/Time Format Examples
DATETIME_FORMAT_EXAMPLES = {
    "iso_format": "2025-09-05T10:00:00Z",
    "date_only": "2025-09-05",
    "time_examples": ["09:00:00", "14:30:00", "16:45:00"]
}

# Patient Field Examples
PATIENT_EXAMPLES = {
    "minimal": {
        "first_name": "John",
        "last_name": "Smith"
    },
    "complete": {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@email.com",
        "date_of_birth": "1985-03-15",
        "title": "Mr",
        "sex": "Male",
        "gender_identity": "Man",
        "address_1": "123 Main Street",
        "city": "London",
        "country": "United Kingdom",
        "post_code": "SW1A 1AA",
        "occupation": "Software Engineer",
        "notes": "Regular patient with no known allergies"
    }
}

# Appointment Field Examples
APPOINTMENT_EXAMPLES = {
    "basic_1_hour": {
        "patient_id": "PATIENT_ID_HERE",
        "practitioner_id": DEFAULT_PRACTITIONER_ID,
        "appointment_type_id": DEFAULT_APPOINTMENT_TYPE_ID,
        "business_id": DEFAULT_BUSINESS_ID,
        "appointment_start": "2025-09-05T10:00:00Z",
        "appointment_end": "2025-09-05T11:00:00Z",
        "notes": "Regular consultation appointment"
    },
    "short_30_min": {
        "patient_id": "PATIENT_ID_HERE",
        "practitioner_id": DEFAULT_PRACTITIONER_ID,
        "appointment_type_id": DEFAULT_APPOINTMENT_TYPE_ID,
        "business_id": DEFAULT_BUSINESS_ID,
        "appointment_start": "2025-09-05T14:00:00Z",
        "appointment_end": "2025-09-05T14:30:00Z",
        "notes": "Follow-up appointment"
    }
}

# Error Prevention Tips for AI Agents
AI_USAGE_TIPS = {
    "patient_lookup": "Always search for existing patients by name before creating new ones",
    "id_format": "All IDs must be strings, not integers (e.g., '1234567890', not 1234567890)",
    "datetime_format": "Use ISO format with 'Z' suffix for UTC times (e.g., '2025-09-05T10:00:00Z')",
    "required_fields": "Check the tool descriptions for REQUIRED vs OPTIONAL fields",
    "validation": "Tools will return helpful error messages with examples if fields are missing"
}

# Quick Reference for AI Agents
QUICK_REFERENCE = {
    "book_appointment_workflow": [
        "1. Search for patient by name using list_patients(q='patient_name')",
        "2. If patient doesn't exist, create using create_patient with first_name and last_name",
        "3. Use create_appointment with all required fields including patient_id from step 1/2",
        "4. Verify appointment was created using get_appointment or list_appointments"
    ],
    "required_appointment_fields": [
        "patient_id (string)",
        "practitioner_id (string - use DEFAULT_PRACTITIONER_ID)",
        "appointment_type_id (string - use DEFAULT_APPOINTMENT_TYPE_ID)", 
        "business_id (string - use DEFAULT_BUSINESS_ID)",
        "appointment_start (ISO datetime string)",
        "appointment_end (ISO datetime string)"
    ]
}
