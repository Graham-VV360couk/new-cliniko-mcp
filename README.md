# Cliniko MCP Server

A Model Context Protocol (MCP) server for integrating with the Cliniko practice management system.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   Create a `.env` file in the project root with your Cliniko API key:
   ```
   CLINIKO_API_KEY=your_actual_cliniko_api_key_here
   ```
   
   To get your API key:
   - Log into your Cliniko account
   - Go to Settings → Integrations → API Keys
   - Create a new API key

3. **Run the Server**
   ```bash
   python main.py
   ```

## Project Structure

```
cliniko_mcp_server/
│
├── .env                    # API key configuration (create this file)
├── main.py                 # Server entry point
├── cliniko_client.py       # Cliniko API client
├── requirements.txt        # Python dependencies
│
├── tools/                  # MCP Tools
│     ├── __init__.py
│     ├── patients.py       # Patient management tools
│     └── appointments.py   # Appointment management tools
│
└── resources/              # MCP Resources
      ├── __init__.py
      └── index.py          # Resource definitions
```

## Available Tools

### Patient Tools
- `list_patients` - List/search all patients
- `get_patient` - Get patient by ID
- `create_patient` - Create new patient
- `update_patient` - Update patient details
- `delete_patient` - Delete (archive) a patient

### Appointment Tools
- `list_appointments` - List/search all appointments
- `get_appointment` - Get appointment by ID
- `create_appointment` - Create new appointment
- `update_appointment` - Update appointment details
- `delete_appointment` - Delete an appointment

## Available Resources

- `patient://{id}` - Get patient by ID
- `patients://list` - List all patients
- `appointment://{id}` - Get appointment by ID
- `appointments://list` - List all appointments

## API Endpoints

The server connects to the Cliniko API at: `https://api.au4.cliniko.com/v1`

## Authentication

Uses Basic Authentication with your Cliniko API key. The key is automatically encoded and included in all API requests.
