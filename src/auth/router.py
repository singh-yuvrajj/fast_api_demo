from datetime import timedelta
import uuid
from annotated_types import T
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import true


from src.auth.schema import UserCreate, UserLogin, UserRead, UserUpdate
from src.auth.service import UserService
from src.auth.utils import create_access_token, verify_password
from src.dependencies import get_user_service

from src.config import get_settings

settings = get_settings()


auth_router = APIRouter()


@auth_router.post("/login", response_model=dict)
async def user_login(
    user_input: UserLogin, user_service: UserService = Depends(get_user_service)
):

    try:

        user = await user_service.get_user_by_username(user_input.username)

        print("Here is the user", user)

        if user and verify_password(user_input.password, user.password):

            user_data = {"user_id": str(user.id), "user_email": user.email}

            access_token = create_access_token(user_data)
            refresh_token = create_access_token(
                user_data,
                expiry=timedelta(days=settings.REFRESH_TOKEN_EXPIRY),
                refresh=true,
            )

            print("Here is the toen", refresh_token)

            response_content = {
                "details": "login successful",
                "user_data": user_data,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

            return JSONResponse(
                content=response_content, status_code=status.HTTP_200_OK
            )

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="incorrect password or username",
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error",
        )


@auth_router.post("/register", response_model=UserRead)
async def register_user(
    user_data: UserCreate, user_service: UserService = Depends(get_user_service)
):

    try:
        user = await user_service.create_user(user_data)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.get("/users", response_model=list[UserRead])
async def get_users(user_service: UserService = Depends(get_user_service)):
    try:
        users = await user_service.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: uuid.UUID, user_service: UserService = Depends(get_user_service)
):
    try:
        user = await user_service.get_user_by_id(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):

    try:
        updated_user = await user_service.update_user(user_id, user_data)
        return updated_user
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@auth_router.delete("/users/{user_id}", response_model=UserRead)
async def delete_user(
    user_id: uuid.UUID, user_service: UserService = Depends(get_user_service)
):
    try:
        user = await user_service.delete_user(user_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
