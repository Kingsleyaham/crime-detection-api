import http
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routers import router as api_router
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.core.exceptions import AppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting up...")
    create_db_and_tables()
    yield
    logging.info("Shutting down database...")


app = FastAPI(
    title="Crime Detection App",
    openapi_url=f"{settings.API_VERSION}/openapi.json",
    version="0.0.1",
    contact={"name": "Aham Kingsley", "email": "kingsleyaham6@gmail.com"},
    lifespan=lifespan
)

# set up CORS
if settings.CORS_ORIGINS:
    app.add_middleware(CORSMiddleware, allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
                       allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# logging.basicConfig(level=logging.ERROR)

# @app.middleware('http')
# async def apply_wrapping(request: Request, call_next):
#     return await success_response_middleware(request, call_next)


# set up routes
app.include_router(api_router, prefix=settings.API_VERSION)


#
# @app.middleware('http')
# async def authenticate_middleware(request: Request, call_next: Callable):
#     response = await authenticate(request, call_next)
#     return response




# Global error handler for unexpected errors
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logging.error(f"unhandled error: {exc}")
    return JSONResponse(
        status_code=exc.status_code if exc.status_code else http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"success": False, "error": exc.message if exc.message else "Internal server error"},
    )


@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to crime detection api"}
