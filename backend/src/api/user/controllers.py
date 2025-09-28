from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.api.user.mappers import UserApiMapper
from src.api.user.schemas import UserResponseSchema, UserCreateSchema
from src.apps.user.use_cases.create_use_case import UserCreateUseCase
from src.apps.user.use_cases.get_by_id_use_case import UserGetByIdUseCase

router = APIRouter(route_class=DishkaRoute, prefix='/user', tags=['User'])


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_by_id(user_id: UUID,
                    use_case: FromDishka[UserGetByIdUseCase]
                    ) -> UserResponseSchema:
    dto = await use_case.execute(user_id)
    return UserApiMapper.dto_to_schema(dto)

@router.post("/")
async def create(user_data: UserCreateSchema,
                 use_case: FromDishka[UserCreateUseCase]
                    ) -> None:
    await use_case.execute(UserApiMapper.schema_to_dto(user_data))

