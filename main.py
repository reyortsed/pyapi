import threading, webbrowser, time
from fastapi import FastAPI, Request
from api.v1.controllers import users, auth
from models.db import metadata
from database import engine
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware
from utils.rate_limiter import limiter

import uvicorn

def open_browser():
    time.sleep(1)
    webbrowser.open("https://127.0.0.1:8000/docs")

threading.Thread(target=open_browser).start()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False, ssl_keyfile="key.pem", ssl_certfile="cert.pem" )
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield  

app = FastAPI(title="PiggyTail", version="1.0.0", lifespan=lifespan)
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(auth.router, prefix="")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )

def custom_openapi():
    from fastapi.openapi.utils import get_openapi
    
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for op in path.values():
            op["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi



