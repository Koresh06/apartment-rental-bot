from typing import Annotated
from fastapi import Depends, APIRouter, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.api_v1.dependenses import admin_auth
from app.core.db_helper import db_helper
from app.tgbot.conf_static import templates



router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
    },
    dependencies=[Depends(admin_auth)],
)


@router.get("/", response_class=HTMLResponse)
async def get_apartments(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
):

    return templates.TemplateResponse("apartaments/home.html", {"request": request})


@router.get('/statistics/', response_class=HTMLResponse)
async def get_statistics(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
):
    return templates.TemplateResponse("statistics.html", {"request": request})


@router.get('/get_users/', response_class=HTMLResponse)
async def get_users(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
):
    return templates.TemplateResponse("get_users.html", {"request": request})

