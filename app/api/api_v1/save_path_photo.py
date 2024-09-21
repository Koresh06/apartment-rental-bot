import os
import shutil
import aiofiles
from typing import List
from datetime import datetime
from uuid import uuid4
from pathlib import Path

from fastapi import UploadFile


from app.core.models.apartament import Apartment
from app.core.models.apartament_photo import ApartmentPhoto

UPLOAD_FOLDER = "app/static/apartaments_photo"


async def create_photo_path(apartment_id: int, filename: str) -> str:
    directory = os.path.join(UPLOAD_FOLDER, str(apartment_id))
    if not os.path.exists(directory):
        os.makedirs(directory)  # Создаем директорию, если она не существует
    return os.path.join(directory, filename).replace("\\", "/")  # Заменяем обратные слеши на прямые

async def save_photos(photos:UploadFile, apartment_id: int) -> List[str]:
    saved_files = []

    for photo in photos:
        if not photo.filename:  # Если имя файла пустое
            continue  # Пропускаем это фото

        # Получаем расширение файла
        extension = os.path.splitext(photo.filename)[1]
        # Генерируем уникальное имя файла
        unique_name = f"{uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}{extension}"
        # Создаем полный путь к файлу
        file_path = await create_photo_path(apartment_id, unique_name)

        # Сохраняем файл на диск
        async with aiofiles.open(file_path, "wb") as f:  # Используем aiofiles для асинхронного открытия файла
            content = await photo.read()  # Чтение содержимого файла
            await f.write(content)  # Асинхронная запись содержимого в файл

        # Сохраняем относительный путь к файлу
        relative_path = os.path.join("apartaments_photo", str(apartment_id), unique_name).replace("\\", "/")
        saved_files.append(relative_path)  # Добавляем относительный путь в список

    return saved_files


def remove_photos(apartament_id: int):
    folder_path = Path('app/static/apartaments_photo') / str(apartament_id)
    
    if folder_path.exists() and folder_path.is_dir():
        shutil.rmtree(folder_path)  # Удаляет папку и всё её содержимое