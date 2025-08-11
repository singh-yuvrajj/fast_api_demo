from typing import Optional
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.utils import decode_token
from src.db.redis import jti_in_blocklist


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:

        creds = await super().__call__(request)

        token = creds.credentials
        token_data = self.validate_token(token)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="expired or invalid token",
            )

        if await jti_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="token has been revoked",
            )

        self.validate_token_data(token_data)

        return token_data

    def validate_token(self, token: str):

        return decode_token(token)

    def validate_token_data(self, token_data: dict):
        raise NotImplementedError("Please override this method in child class")


class AccessTokenBearer(TokenBearer):

    def validate_token_data(self, token_data: dict):

        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide accesss token",
            )

        return True


class RefreshTokenBearer(TokenBearer):

    def validate_token_data(self, token_data: dict):

        if not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide refresh token",
            )

        return True
