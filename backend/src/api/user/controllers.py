from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.api.user.mappers import UserApiMapper
from src.api.user.schemas import UserCreateSchema, UserResponseSchema
from src.apps.user.use_cases.create_use_case import UserCreateUseCase
from src.apps.user.use_cases.get_by_id_use_case import UserGetByIdUseCase
from src.core.bg_tasks.tasks import send_email_task

router = APIRouter(route_class=DishkaRoute)


@router.get("/{user_id}", status_code=200, response_model=UserResponseSchema)
async def get_by_id(user_id: UUID, use_case: FromDishka[UserGetByIdUseCase]) -> UserResponseSchema:
    dto_out = await use_case.execute(user_id)
    return UserApiMapper.dto_to_schema(dto_out)


# TODO установить ResponseSchema
@router.post("/", status_code=201, response_model=UserResponseSchema)
async def create(
    user_data: UserCreateSchema,
    use_case: FromDishka[UserCreateUseCase],
) -> UserResponseSchema:
    dto_out = await use_case.execute(UserApiMapper.schema_to_dto(user_data))
    await send_email_task.kiq(data=dto_out.email)
    return UserApiMapper.dto_to_schema(dto_out)
