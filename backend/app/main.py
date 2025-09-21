from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import settings

app = FastAPI(
    title="AutoApply Assistant API",
    description="API for managing the AutoApply Assistant backend logic, including AI, automation, and data management.",
    version="0.1.0",
)

# CORS (Cross-Origin Resource Sharing) Middleware
# This allows the frontend (running on localhost:3000) to communicate with the backend.
origins = [
    "http://localhost:3000", # React default dev server
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(settings.router, prefix="/api")


@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"status": "ok", "message": "Welcome to AutoApply Assistant API"}
