from fastapi import APIRouter, HTTPException, status, Body
from ..models.settings import ApiKey
from ..core.security import save_api_key, get_api_key, delete_api_key

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)

@router.post("/api-key", status_code=status.HTTP_201_CREATED)
def set_api_key(api_key_data: ApiKey):
    """
    Saves an API key securely in the OS keychain.
    """
    if not api_key_data.service_name or not api_key_data.api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service name and API key cannot be empty."
        )
    try:
        save_api_key(api_key_data.service_name, api_key_data.api_key)
        return {"message": f"API key for '{api_key_data.service_name}' saved successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save API key: {e}"
        )

@router.get("/api-key/{service_name}", response_model=dict)
def check_api_key(service_name: str):
    """
    Checks if an API key for a given service exists.
    Does not return the key itself for security.
    """
    key = get_api_key(service_name)
    return {"service_name": service_name, "exists": key is not None}

@router.delete("/api-key/{service_name}", status_code=status.HTTP_200_OK)
def remove_api_key(service_name: str):
    """
    Deletes an API key from the OS keychain.
    """
    try:
        delete_api_key(service_name)
        return {"message": f"API key for '{service_name}' deleted successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete API key: {e}"
        )
