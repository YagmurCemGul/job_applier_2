from pydantic import BaseModel

class ApiKey(BaseModel):
    """Pydantic model for API key data transfer."""
    service_name: str
    api_key: str
