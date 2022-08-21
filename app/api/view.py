from fastapi import APIRouter
from app.static import google_login_javascript_client, google_login_javascript_server
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/google_login_client", tags=["security"])
def google_login_client():
    return HTMLResponse(google_login_javascript_client)


@router.get("/google_login_server", tags=["security"])
def google_login_server():
    return HTMLResponse(google_login_javascript_server)
