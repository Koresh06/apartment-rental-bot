from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from app.api.api_v1.routers.user_router import router as user_router
from app.api.api_v1.routers.apartament_router import router as apartament_router
from app.api.api_v1.routers.auth_router import router as auth_router
from app.tgbot.conf_static import configure_static

app = FastAPI()

configure_static(app)


@app.get("/")
async def root():
    return RedirectResponse(
        url="/auth/login",
        status_code=status.HTTP_302_FOUND,
    )

# Включение роутеров FastAPI
app.include_router(auth_router)
app.include_router(apartament_router)
app.include_router(user_router)
