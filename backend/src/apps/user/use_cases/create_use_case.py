from src.apps.interfaces import IEmailNotificationService
from src.apps.user.irepo import IUserRepository
from src.domain.user import PasswordHashVo
from src.domain.user.dtos import UserInputDto, UserOutputDto
from src.domain.user.interfaces import IPasswordHasher
from src.domain.user.mappers import UserDomainMapper
from src.domain.user.value_objects import UserFirstNameVo


class UserCreateUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        hasher: IPasswordHasher,
        email_notification_service: IEmailNotificationService,
    ):
        self.user_repo = user_repo
        self.hasher = hasher
        self.email_notification_service = email_notification_service

    # TODO: добавить обработку ошибок
    async def execute(self, dto: UserInputDto) -> UserOutputDto:
        existing_user_entity = await self.user_repo.get_by_email(dto.email)
        if existing_user_entity:
            # TODO: Рейзить ошибку что пользак есть в БД
            # raise UserAlreadyExistsError(dto.email)
            # TODO: ВРЕМЕННО чтобы тип вернуть ошибку в поле first_name -> Удалить потом!!!
            existing_user_entity.first_name = UserFirstNameVo("Email УЖЕ СУЩЕСТВУЕТ!!!")
            return UserDomainMapper.entity_to_output_dto(existing_user_entity)

        password_vo = PasswordHashVo.from_plain(plain=dto.password, hasher=self.hasher)
        user_entity = UserDomainMapper.input_dto_to_entity(dto=dto, password_vo=password_vo)
        await self.user_repo.save(user_entity)

        data = user_entity.email.value
        # TODO: обсудить! будем отправлять на email приветствие? или пока taskiq выкл
        await self.email_notification_service.send_email(
            to_email="a.zubchyk@miran-bel.com",
            data=data,
        )

        return UserDomainMapper.entity_to_output_dto(user_entity)
