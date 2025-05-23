from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/callback")
def oauth_callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    error = request.query_params.get("error_description")
    return {
        "message": error,
        "code": code,
        "state": state
    }
