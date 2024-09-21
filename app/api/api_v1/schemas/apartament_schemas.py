from datetime import date, time
from typing import Annotated, List, Optional
from pydantic import BaseModel
from fastapi import File, Form, UploadFile




class CreateApartmentSchema(BaseModel):
    location: str
    rooms: int
    price: int
    description: str
    photos: List[UploadFile]
    features: Optional[List[str]] = None

    @classmethod
    async def create(
        cls,
        location: str = Form(...),
        rooms: int = Form(...),
        price: int = Form(...),
        description: str = Form(...),
        photos: List[UploadFile] = File(...),
        features: Optional[List[str]] = Form(None),
    ) -> "CreateApartmentSchema":
        return cls(
            location=location,
            rooms=rooms,
            price=price,
            description=description,
            photos=photos,
            features=features,
        )