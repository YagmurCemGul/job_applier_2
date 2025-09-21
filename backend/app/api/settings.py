from fastapi import APIRouter, HTTPException, status, Body
from ..models.settings import ServiceCredential
from ..core.security import save_credential, get_credential, delete_credential

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)

@router.post("/credential", status_code=status.HTTP_201_CREATED)
def set_credential(credential_data: ServiceCredential):
    """
    Saves a service credential (username and password) securely in the OS keychain.
    """
    if not all([credential_data.service_name, credential_data.username, credential_data.password]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service name, username, and password cannot be empty."
        )
    try:
        save_credential(credential_data.service_name, credential_data.username, credential_data.password)
        return {"message": f"Credential for '{credential_data.username}' on service '{credential_data.service_name}' saved."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save credential: {e}"
        )

@router.get("/credential/{service_name}/{username}", response_model=dict)
def check_credential(service_name: str, username: str):
    """
    Checks if a credential for a given service and username exists.
    Does not return the password itself for security.
    """
    password = get_credential(service_name, username)
    return {"service_name": service_name, "username": username, "exists": password is not None}

@router.delete("/credential/{service_name}/{username}", status_code=status.HTTP_200_OK)
def remove_credential(service_name: str, username: str):
    """
    Deletes a credential from the OS keychain.
    """
    try:
        delete_credential(service_name, username)
        return {"message": f"Credential for '{username}' on service '{service_name}' deleted."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete credential: {e}"
        )
