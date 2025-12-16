from fastapi import APIRouter
from versions.versions import (
    save_version,
    get_version_history,
    get_version,
    delete_version,
    clear_versions,
)

router = APIRouter(prefix="/versions", tags=["Versions"])

# SAVE VERSION
@router.post("/save")
def api_save_version(payload: dict):
    return save_version(**payload)

# GET SINGLE VERSION 
@router.get("/version/{version_id}")
def api_get_version(version_id: int):
    return get_version(version_id)

# DELETE SINGLE VERSION
@router.delete("/version/{version_id}")
def api_delete_version(version_id: int):
    return delete_version(version_id)

# GET VERSION HISTORY 
@router.get("/{session_id}")
def api_get_version_history(session_id: str):
    return get_version_history(session_id)

# CLEAR ALL VERSIONS FOR SESSION
@router.delete("/{session_id}")
def api_clear_versions(session_id: str):
    return clear_versions(session_id)
