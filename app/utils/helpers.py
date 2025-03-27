from fastapi import HTTPException


def extract_bearer_token(header:str) ->str:
    parts = header.split()
    if(len(parts) != 2) or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    return parts[1]