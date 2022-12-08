# OCCP Central System Server

A project for implementing a server that functions as a Central System for chargers (Charging Points) and Users making
use of OCCP protocol.

## Development Instructions

0. Make sure to have a virtual environment activated.
1. Install python requirements: ```pip install -r requirements.txt```
2. Start server with: ```uvicorn main:app --reload```

### REST Endpoints

- / : List all Charge Points

### WS Endpoints

- /ws/{cp_id} : Connect with a Charge Point


