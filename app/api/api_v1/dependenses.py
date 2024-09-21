from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.auth_helpers import ADMIN_LOGIN, SECRET_KEY, verify_hashed_cookie
from app.core.db_helper import db_helper
from app.core.models.user import Users


async def admin_auth(request: Request):
    admin_token = request.cookies.get("admin_token")
    if admin_token is None or not verify_hashed_cookie(admin_token, ADMIN_LOGIN, SECRET_KEY):
        raise HTTPException(status_code=302, detail="Redirecting to login", headers={"Location": "/auth/login"})
    return True
    # admin_token = request.cookies.get("admin_token")
    # if admin_token is None or not verify_hashed_cookie(admin_token, ADMIN_LOGIN, SECRET_KEY):
    #     return None
    # return True
