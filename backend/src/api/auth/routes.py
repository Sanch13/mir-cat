from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.api.user.mappers import UserApiMapper
from src.api.user.schemas import UserAuthSchema
from src.apps.user.use_cases.auth_use_case import AuthUserUseCase

router = APIRouter(route_class=DishkaRoute)


@router.post("/login", status_code=200)
async def login_user(
    auth_dto: UserAuthSchema,
    use_case: FromDishka[AuthUserUseCase],
) -> dict[str, str]:
    return await use_case.execute(dto=UserApiMapper.user_auth_schema_to_dto(auth_dto))
