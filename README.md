# FastAPI User Management API

A get you going FastAPI application with CRUD operations for user management.
Protect the controllers by adding an _ANY = depends(get_current_user) - currently removed for ease of development
You will need to register API in Azure, and a client and generate the jwt token. 

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --host=127.0.0.1 --port=8000 --reload=True  --ssl_keyfile=key.pem --ssl_certfile=cert.pem 
```
There is also an entry point allowing for easy debugging. Make sure reload is False for debugging, otherwise seperate threads are spawned outside controller of debugger

uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False, ssl_keyfile="key.pem", ssl_certfile="cert.pem" )


3. Access the API documentation:
- Swagger UI: https://localhost:8000/docs
- ReDoc: https://localhost:8000/redoc

## API Endpoints

- GET /users/ - List all users
- GET /users/{user_id} - Get a specific user
- POST /users/ - Create a new user
- PATCH /users/{user_id} - Update a user
- DELETE /users/{user_id} - Delete a user
