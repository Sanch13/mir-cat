from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response

from src.application.auth.use_case.auth_use_case import AuthUserUseCase
from src.presentation.api.auth.mappers import AuthUserApiMapper
from src.presentation.api.auth.schemas import TokenOutSchema, UserAuthSchema

router = APIRouter(route_class=DishkaRoute)


@router.post("/login", status_code=200, response_model=TokenOutSchema)
async def login_user(
    request: Request,
    response: Response,
    auth_dto: UserAuthSchema,
    use_case: FromDishka[AuthUserUseCase],
) -> TokenOutSchema:
    meta = {
        "ip": request.client.host if request.client else "",
        "ua": request.headers.get("user-agent", ""),
    }

    data_out = await use_case.execute(
        dto=AuthUserApiMapper.user_auth_schema_to_dto(auth_dto),
        meta=meta,
    )

    refresh_token = data_out.pop("refresh_token", "string")
    max_age = data_out.pop("expires_in_refresh", 604800)

    # ставим refresh в HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # в dev можно False, в проде True (только по HTTPS)
        samesite="strict",  # lax удобнее для обычных навигаций; strict — самый безопасный.
        path="/auth/refresh",  # ограничить область действия cookie
        max_age=max_age,
    )
    return AuthUserApiMapper.dict_to_schema(data_out)
