import uuid
from fastapi import APIRouter, Depends, HTTPException

from src.auth.schema import UserCreate, UserRead, UserUpdate
from src.auth.service import UserService
from src.dependencies import get_user_service


auth_router = APIRouter()


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
        updated_user = user_service.update_user(user_id, user_data)
        return updated_user
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@auth_router.delete("/users/{user_id}", response_model=UserRead)
async def delete_user(
    user_id: uuid.UUID, user_service: UserService = Depends(get_user_service)
):
    try:
        user = user_service.delete_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
