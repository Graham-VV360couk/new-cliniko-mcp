# Cliniko MCP Server - AI Agent Usage Guide

This guide is specifically designed for AI agents (like Eleven Labs conversational AI) to ensure reliable, first-try success when using Cliniko MCP tools.

## ⚡ Quick Success Patterns

### 1. Booking an Appointment (Most Common Use Case)

**Step-by-step workflow:**
```python
# Step 1: Find the patient
list_patients(q="John Smith")

# Step 2: If patient not found, create them
create_patient({
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@email.com"  # optional but recommended
})

# Step 3: Book appointment (use EXACT format below)
create_appointment({
    "patient_id": "1764028746571981724",  # From step 1 or 2
    "practitioner_id": "1752849161776013508",  # Default practitioner
    "appointment_type_id": "1752849165005627509",  # Default appointment type
    "business_id": "1752849165332784051",  # Default business
    "appointment_start": "2025-09-05T10:00:00Z",  # ISO format with Z
    "appointment_end": "2025-09-05T11:00:00Z",    # ISO format with Z
    "notes": "Regular consultation"  # Optional
})
```

### 2. Critical Field Formats

**All IDs MUST be strings:**
```json
✅ CORRECT: "1764028746571981724"
❌ WRONG: 1764028746571981724
```

**DateTime MUST be ISO format with Z:**
```json
✅ CORRECT: "2025-09-05T10:00:00Z"
❌ WRONG: "2025-09-05 10:00:00"
❌ WRONG: "September 5th, 2025 at 10am"
```

### 3. Default Values (Use These Always)

```python
DEFAULT_PRACTITIONER_ID = "1752849161776013508"
DEFAULT_APPOINTMENT_TYPE_ID = "1752849165005627509"  
DEFAULT_BUSINESS_ID = "1752849165332784051"
```

## 🛡️ Error Prevention Rules

### Rule 1: Always Search Before Creating
```python
# ALWAYS do this first
patients = list_patients(q="John Smith")
if not patients["patients"]:
    # Only create if not found
    patient = create_patient({"first_name": "John", "last_name": "Smith"})
```

### Rule 2: Use Exact Field Names
```python
# Appointments - Use these EXACT field names:
{
    "patient_id": "string",           # NOT "patient" or "patientId"
    "practitioner_id": "string",      # NOT "practitioner" or "doctor_id"
    "appointment_type_id": "string",  # NOT "type" or "appointment_type"
    "business_id": "string",          # NOT "business" or "clinic_id"
    "appointment_start": "string",    # NOT "start_time" or "starts_at"
    "appointment_end": "string"       # NOT "end_time" or "ends_at"
}
```

### Rule 3: Handle Time Calculations
```python
# For 1-hour appointment starting at 10 AM:
start_time = "2025-09-05T10:00:00Z"
end_time = "2025-09-05T11:00:00Z"  # Add 1 hour

# For 30-minute appointment:
start_time = "2025-09-05T14:00:00Z" 
end_time = "2025-09-05T14:30:00Z"   # Add 30 minutes
```

## 📋 Complete Tool Reference

### Patient Tools

**list_patients(q="")**
- `q`: Search query (empty string for all patients)
- Returns: `{"patients": [...]}`

**get_patient(patient_id)**
- `patient_id`: String ID (e.g., "1764028746571981724")
- Returns: Patient object

**create_patient(patient)**
- Required: `first_name`, `last_name`
- Optional: `email`, `date_of_birth`, `title`, `sex`, etc.
- Returns: Created patient object

### Appointment Tools

**list_appointments(q="")**
- `q`: Search query (empty string for all appointments)
- Returns: `{"appointments": [...]}`

**get_appointment(appointment_id)**
- `appointment_id`: String ID (e.g., "1764031489109926340")
- Returns: Appointment object

**create_appointment(appointment)**
- Required: `patient_id`, `practitioner_id`, `appointment_type_id`, `business_id`, `appointment_start`, `appointment_end`
- Optional: `notes`
- Returns: Created appointment object

## 🔧 Common Conversation Patterns

### Pattern 1: "Book John Smith for tomorrow at 3pm"
```python
# 1. Calculate tomorrow's date in ISO format
tomorrow_3pm = "2025-09-06T15:00:00Z"
tomorrow_4pm = "2025-09-06T16:00:00Z"

# 2. Find patient
patients = list_patients(q="John Smith")
patient_id = patients["patients"][0]["id"] if patients["patients"] else None

# 3. Create if needed
if not patient_id:
    patient = create_patient({"first_name": "John", "last_name": "Smith"})
    patient_id = patient["id"]

# 4. Book appointment
appointment = create_appointment({
    "patient_id": patient_id,
    "practitioner_id": "1752849161776013508",
    "appointment_type_id": "1752849165005627509",
    "business_id": "1752849165332784051", 
    "appointment_start": tomorrow_3pm,
    "appointment_end": tomorrow_4pm,
    "notes": "Appointment booked via AI assistant"
})
```

### Pattern 2: "Show me all appointments for next week"
```python
# List all appointments (Cliniko will return recent/upcoming)
appointments = list_appointments(q="")
# Filter by date range if needed in your application logic
```

### Pattern 3: "Cancel appointment ID 12345"
```python
# Delete the appointment
result = delete_appointment("12345")
```

## ⚠️ Critical Don'ts

1. **Don't use integer IDs** - Always strings
2. **Don't guess field names** - Use exact names from this guide
3. **Don't use natural language dates** - Always ISO format
4. **Don't skip required fields** - Include all 6 required fields for appointments
5. **Don't create duplicate patients** - Always search first

## ✅ Success Validation

After each operation, verify success:
```python
# After creating appointment
appointment = create_appointment(appointment_data)
if "id" in appointment:
    print(f"✅ Appointment created with ID: {appointment['id']}")
else:
    print(f"❌ Error: {appointment}")
```

## 🎯 Performance Tips for Eleven Labs

1. **Pre-load common data** - Cache practitioner and business IDs
2. **Batch operations** - Get patient info and appointment creation in sequence
3. **Use descriptive names** - Help users understand what's happening
4. **Validate inputs early** - Check date formats before API calls

## 📞 Example Conversation Flow

**User:** "Book Sarah Johnson for a checkup on Friday at 2 PM"

**AI Response Pattern:**
1. "Let me search for Sarah Johnson in the system..."
2. "Found Sarah Johnson. Now booking appointment for Friday at 2 PM..."
3. "✅ Appointment confirmed! Sarah Johnson is booked for Friday, [DATE] at 2:00 PM with Dr. Yash Verma."

This ensures the user knows what's happening and feels confident in the booking.
