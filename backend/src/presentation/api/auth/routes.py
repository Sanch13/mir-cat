from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from src.application.auth.use_case.auth_use_case import AuthUserUseCase
from src.presentation.api.auth.mappers import AuthUserApiMapper
from src.presentation.api.auth.schemas import UserAuthSchema

router = APIRouter(route_class=DishkaRoute)


@router.post("/login", status_code=200)
async def login_user(
    auth_dto: UserAuthSchema,
    use_case: FromDishka[AuthUserUseCase],
) -> dict[str, str]:
    return await use_case.execute(dto=AuthUserApiMapper.user_auth_schema_to_dto(auth_dto))
