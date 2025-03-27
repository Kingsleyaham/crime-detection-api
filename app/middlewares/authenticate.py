import jwt
from fastapi import Request, Response
from typing import Callable

from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.helpers import extract_bearer_token


async def authenticate(request: Request, call_next: Callable):
    public_routes: list[str] = ['/', '/auth/login', '/auth/signup']

    print(request.url.path)

    if request.url.path in public_routes:
        return await call_next(request)
    else:
        header = request.headers.get('Authorization')
        if not header or not header.startswith('Bearer '):
            return JSONResponse(status_code=401, content={"success": False, "error": 'Invalid or Missing token'})
        token = extract_bearer_token(header)
        try:
            request.state.user = await jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"success": False, "error": 'Invalid token'})
        return await call_next(request)
