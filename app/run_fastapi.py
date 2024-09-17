from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

# from app.tgbot.api.routers.lesson_router import router as lessons_router
# from app.tgbot.api.routers.user_router import router as users_router
from app.tgbot.conf_static import configure_static

app = FastAPI()

configure_static(app)


# @app.get("/")
# async def root():
#     return RedirectResponse(
#         url="/lessons/get-lessons",
#         status_code=status.HTTP_302_FOUND,
#     )

# Включение роутеров FastAPI
# app.include_router(lessons_router)
# app.include_router(users_router)