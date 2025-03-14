from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.configs.config import settings
from app.databases.init_postgresql import Base, engine, init_db
from app.routers.main import app_router

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.on_event("startup")
async def startup():
    init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_router)


@app.exception_handler(Exception)
def custom_exception_handler(_: Request, exc: Exception):
    status_code = getattr(exc, "status_code", HTTPStatus.INTERNAL_SERVER_ERROR)
    message = getattr(exc, "message", HTTPStatus.INTERNAL_SERVER_ERROR.phrase)

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
            "code": status_code,
        },
    )


@app.exception_handler(404)
def not_found_handler(request: Request, _: Exception):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": f"Cannot find {request.url.path} on this server",
            "code": 404,
        },
    )
