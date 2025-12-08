from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Cookie, Depends, Request, Response, status
from fastapi.security import HTTPBearer

from src.application.auth.use_case.auth_use_case import AuthUserUseCase
from src.application.auth.use_case.logout_use_case import LogoutUseCase
from src.application.auth.use_case.refresh_token_use_case import RefreshTokenUseCase
from src.infrastructure.services.current_user.current_user_service import GetCurrentUserService
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
        secure=False,  # в dev можно False, в проде True (только по HTTPS)
        samesite="strict",  # lax удобнее для обычных навигаций; strict — самый безопасный.
        path="/api/v1/auth",  # ограничить область действия cookie
        max_age=max_age,
    )
    return AuthUserApiMapper.dict_to_schema(data_out)


@router.post("/refresh", status_code=200, response_model=TokenOutSchema)
async def refresh(
    response: Response,
    use_case: FromDishka[RefreshTokenUseCase],
    refresh_token: str | None = Cookie(None),
):  # TODO: Переписать refresh_token: str | None = Cookie(None) на  реквест
    data_out = await use_case.execute(refresh_token=refresh_token)
    print(data_out)

    refresh_token = data_out.pop("refresh_token", "string")
    max_age = data_out.pop("expires_in_refresh", 604800)

    # ставим refresh в HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # в dev можно False, в проде True (только по HTTPS)
        samesite="strict",  # lax удобнее для обычных навигаций; strict — самый безопасный.
        path="/api/v1/auth",  # ограничить область действия cookie
        max_age=max_age,
    )
    return AuthUserApiMapper.dict_to_schema(data_out)


@router.post(
    path="/logout",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(HTTPBearer(auto_error=False))],
)
async def logout(
    request: Request,
    auth_jwt_service: FromDishka[GetCurrentUserService],
    use_case: FromDishka[LogoutUseCase],
    refresh_token: str | None = Cookie(None),
) -> dict:
    """
    Выход из системы.
    """
    payload = await auth_jwt_service.get_payload_from_access_token(request)
    await auth_jwt_service.is_access_token_in_blacklist(payload)
    access_jti = payload.get("jti")
    return await use_case.execute(access_jti, refresh_token=refresh_token)
