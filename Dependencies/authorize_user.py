from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from datetime import datetime, timezone
from Exceptions.authorization_exceptions import AuthorizationException

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM ="HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def authorize_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data = {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "account_type": payload.get("account_type"),
            "company_id": payload.get("company_id"),
            "iat": payload.get("iat"),
            "exp": payload.get("exp")
        }
        # Validate expiration
        if "exp" in payload:
            if datetime.fromtimestamp(payload["exp"], tz=timezone.utc) < datetime.now(timezone.utc):
                raise AuthorizationException()
            
        return user_data
    except jwt.ExpiredSignatureError:
        raise AuthorizationException()
    except jwt.PyJWTError:
        raise Exception()
        # raise AuthorizationException("Invalid token")