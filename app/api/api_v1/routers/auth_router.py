from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from datetime import timedelta
from app.api.api_v1.auth_helpers import (
    ADMIN_LOGIN,
    ADMIN_PASSWORD,
    SECRET_KEY,
    create_hashed_cookie,
    verify_hashed_cookie,
)
from app.api.api_v1.dependenses import admin_auth
from app.tgbot.conf_static import templates

from app.core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# OAuth2 схема
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse(
        "auth_login.html",
        {
            "request": request,
            # "user": is_authenticated,
        },
    )


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    try:
        if not (username == ADMIN_LOGIN and password == ADMIN_PASSWORD):
            msg = "Incorrect Username or Rassword"
            return templates.TemplateResponse(
                "auth_login.html",
                {
                    "request": request,
                    "msg": msg,
                },
            )
        else:
        # Генерация зашифрованной куки
            hashed_cookie = create_hashed_cookie(username, SECRET_KEY)
            response = RedirectResponse(url="/users/",  status_code=status. HTTP_302_FOUND)
            # Устанавливаем зашифрованную куку
            response.set_cookie(
                key="admin_token", value=hashed_cookie, httponly=True, max_age=1800
            )
        return response
    except HTTPException as e:
        msg = "Unknown Error"
        return templates.TemplateResponse(
            "auth_login.html",
            {
                "request": request,
                "msg": msg,
            },
        )


# Выход (удаление куки)
@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("admin_token")
    return response
