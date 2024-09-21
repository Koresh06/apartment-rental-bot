from typing import Annotated, List, Optional
from fastapi import Depends, APIRouter, File, Form, HTTPException, Request, UploadFile, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.api_v1.dependenses import admin_auth
from app.api.api_v1.save_path_photo import remove_photos, save_photos
from app.api.api_v1.schemas.apartament_schemas import CreateApartmentSchema
from app.api.api_v1.services.apartament_service import ApartamentRepo
from app.api.api_v1.services.apartament_photo_service import ApartamentPhotoRepo
from app.core.db_helper import db_helper
from app.core.models.apartament import Apartment
from app.core.models.apartament_photo import ApartmentPhoto
from app.tgbot.conf_static import templates


router = APIRouter(
    prefix="/apartaments",
    tags=["apartaments"],
    responses={
        404: {"description": "Not found"},
    },
    dependencies=[Depends(admin_auth)],
)


@router.get("/get_apartaments/", response_class=HTMLResponse)
async def get_apartaments(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.get_db)],
):
    apartaments = await ApartamentRepo(session).get_apartaments()

    return templates.TemplateResponse(
        "apartaments/get_apartaments.html",
        {
            "request": request,
            "apartaments": apartaments,
        },
    )

@router.get("/create_apartament/", response_class=HTMLResponse)
async def create_apartament(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
):
    return templates.TemplateResponse(
        "apartaments/create_apartament.html", {"request": request}
    )


@router.post("/create_apartament/")
async def create_apartament(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_db),
    ],
    create_apartment: CreateApartmentSchema = Depends(CreateApartmentSchema.create),
):
    new_apartament = Apartment(
        location=create_apartment.location,
        price=create_apartment.price,
        rooms=create_apartment.rooms,
        description=create_apartment.description,
        characteristics=create_apartment.features,
    )
    await ApartamentRepo(session).create_apartament(new_apartament)

    saved_photos = await save_photos(
        create_apartment.photos, new_apartament.id
    )

    for photo_path in saved_photos:
        apartment_photo = ApartmentPhoto(
            apartment_id=new_apartament.id,
            file_path=photo_path,
        )
        await ApartamentPhotoRepo(session).add_path_photo_apartament(apartment_photo)

    return RedirectResponse("/apartaments/get_apartaments/", status_code=303)


@router.get("/get_apartament/{apartament_id}/", response_class=HTMLResponse)
async def get_apartament(
    request: Request,
    apartament_id: int,
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.get_db),
    ],
):
    apartament = await ApartamentRepo(session).get_aptament_by_id(apartament_id)

    return templates.TemplateResponse(
        "apartaments/get_apartament_id.html",
        {
            "request": request,
            "apartament": apartament,
        },
    )

@router.post("/update_status/{apartament_id}/")
async def update_status(
    apartament_id: int,
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.get_db),
    ],
):
    await ApartamentRepo(session).update_status(apartament_id)
    return RedirectResponse(f"/apartaments/get_apartament/{apartament_id}/", status_code=303)



@router.get("/edit_apartament/{apartament_id}/", response_class=HTMLResponse)
async def update_apartament(
    request: Request,
    apartament_id: int,
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.get_db),
    ],
):
    apartament = await ApartamentRepo(session).get_aptament_by_id(apartament_id)

    return templates.TemplateResponse(
        "apartaments/edit_apartament.html",
        {
            "request": request,
            "apartament": apartament,
        },
    )


@router.post("/edit_apartament/{apartament_id}/")
async def update_apartament(
    apartament_id: int,
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.get_db),
    ],  
    create_apartment: CreateApartmentSchema = Depends(CreateApartmentSchema.create),
):

    data = Apartment(
        location=create_apartment.location,
        price=create_apartment.price,
        rooms=create_apartment.rooms,
        description=create_apartment.description,
        characteristics=create_apartment.features,
    )
    await ApartamentRepo(session).update_apartament_id(apartament_id, data)

    if not create_apartment.photos or all(photo.filename == '' for photo in create_apartment.photos):
        print("Фотографии не переданы или они пустые.")
        return RedirectResponse(f"/apartaments/get_apartament/{apartament_id}/", status_code=303)

    await ApartamentPhotoRepo(session).delete_photos_by_apartment_id(apartament_id)

    new_photos_paths = await save_photos(create_apartment.photos, apartament_id)


    # Сохраняем новые пути к фотографиям в базу данных
    for photo_path in new_photos_paths:
        apartament_photo = ApartmentPhoto(
            apartment_id=apartament_id,
            file_path=photo_path,
        )
        await ApartamentPhotoRepo(session).add_path_photo_apartament(apartament_photo)

    return RedirectResponse(f"/apartaments/get_apartament/{apartament_id}/", status_code=303)


@router.post("/delete_apartament/{apartament_id}/")
async def delete_apartament(
    apartament_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.get_db)],
):
    # Получаем апартамент из базы данных
    apartament = await ApartamentRepo(session).get_aptament_by_id(apartament_id)
    
    if not apartament:
        raise HTTPException(status_code=404, detail="Апартамент не найден")

    await ApartamentPhotoRepo(session).delete_photos_by_apartment_id(apartament_id)

    # Удаляем сам апартамент из базы данных
    await ApartamentRepo(session).delete_apartament(apartament_id)

    # Перенаправление на страницу со списком апартаментов
    return RedirectResponse(url="/apartaments/get_apartaments/", status_code=303)
