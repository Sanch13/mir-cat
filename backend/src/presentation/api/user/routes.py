from uuid import UUID

import structlog
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer

from src.application.user.use_cases.create_use_case import UserCreateUseCase
from src.application.user.use_cases.get_by_id_use_case import UserGetByIdUseCase
from src.infrastructure.services.current_user.current_user_service import GetCurrentUserService
from src.presentation.api.user.mappers import UserApiMapper
from src.presentation.api.user.schemas import UserCreateSchema, UserResponseSchema

router = APIRouter(route_class=DishkaRoute)

logger = structlog.get_logger()


@router.post("/", status_code=201, response_model=UserResponseSchema)
async def create(
    user_data: UserCreateSchema,
    use_case: FromDishka[UserCreateUseCase],
) -> UserResponseSchema:
    log = logger.bind(email=user_data.email, action="create_user")
    log.info("api_request_received")
    dto_out = await use_case.execute(UserApiMapper.schema_to_dto(user_data))
    log.info("api_request_finished", user_id=str(dto_out.id))
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
    auth_jwt_service: FromDishka[GetCurrentUserService],
) -> UserResponseSchema:
    log = logger.bind(action="get_user_by_id")
    log.info("routes_get_user_by_id_started")
    user_id = await auth_jwt_service.get_current_user_id(request)
    log.info(user_id=str(user_id))
    dto_out = await use_case.execute(user_id)
    log.info("routes_get_user_by_id_finished")
    return UserApiMapper.dto_to_schema(dto_out)


@router.get("/{user_id}", status_code=200, response_model=UserResponseSchema)
async def get_by_id(user_id: UUID, use_case: FromDishka[UserGetByIdUseCase]) -> UserResponseSchema:
    dto_out = await use_case.execute(user_id)
    return UserApiMapper.dto_to_schema(dto_out)
