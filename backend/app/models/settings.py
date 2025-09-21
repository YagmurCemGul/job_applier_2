from pydantic import BaseModel, Field

class ServiceCredential(BaseModel):
    """Pydantic model for service credential data transfer."""
    service_name: str = Field(..., description="The name of the service (e.g., 'openai', 'google')")
    username: str = Field(..., description="The username or email for the service account.")
    password: str = Field(..., description="The password for the service account.")
