from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer

from src.api.user.mappers import UserApiMapper
from src.api.user.schemas import UserCreateSchema, UserResponseSchema
from src.apps.user.services.get_user_service import GetCurrentUserService
from src.apps.user.use_cases.create_use_case import UserCreateUseCase
from src.apps.user.use_cases.get_by_id_use_case import UserGetByIdUseCase

router = APIRouter(route_class=DishkaRoute)


@router.post("/", status_code=201, response_model=UserResponseSchema)
async def create(
    user_data: UserCreateSchema,
    use_case: FromDishka[UserCreateUseCase],
) -> UserResponseSchema:
    dto_out = await use_case.execute(UserApiMapper.schema_to_dto(user_data))
    return UserApiMapper.dto_to_schema(dto_out)


@router.get(
    path="/me",
    status_code=200,
    response_model=UserResponseSchema,
    dependencies=[Depends(HTTPBearer(auto_error=False))],
)
async def get_user_by_id(
    request: Request,
    use_case: FromDishka[UserGetByIdUseCase],
    auth_service: FromDishka[GetCurrentUserService],
) -> UserResponseSchema:
    user_id = await auth_service.get_current_user_id(request)
    dto_out = await use_case.execute(user_id)
    return UserApiMapper.dto_to_schema(dto_out)


@router.get("/{user_id}", status_code=200, response_model=UserResponseSchema)
async def get_by_id(user_id: str, use_case: FromDishka[UserGetByIdUseCase]) -> UserResponseSchema:
    dto_out = await use_case.execute(user_id)
    return UserApiMapper.dto_to_schema(dto_out)
