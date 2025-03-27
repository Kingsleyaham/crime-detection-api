import http
import json
import logging

from typing import Callable

from fastapi import Request
from starlette.responses import JSONResponse, StreamingResponse


async def success_response_middleware(request: Request, call_next: Callable, ):
    response = await call_next(request)



    # Only process successful JSON response (2xx status codes)
    if http.HTTPStatus(response.status_code).is_success:
        content_type: str = response.headers.get('content-type', "")

        if "application/json" in content_type.lower():
            try:
                # Read response body correctly
                if isinstance(response, (JSONResponse, JSONResponse)):
                    original_body = response.body
                elif isinstance(response, StreamingResponse):
                    original_body = b"".join([chunk async for chunk in response.body_iterator])
                else:
                    return response

                original_data = json.loads(original_body.decode("utf-8"))

                # Wrap response in standard format
                wrapped_response = {
                    "success": True,
                    "data": original_data
                }

                return JSONResponse(
                    content=wrapped_response,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )
            except (json.JSONDecodeError, AttributeError):
                pass

    return response
