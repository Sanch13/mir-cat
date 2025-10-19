from pwdlib import PasswordHash

from src.domain.user.interfaces import IPasswordHasher


class PasswordHasherImpl(IPasswordHasher):
    def __init__(self) -> None:
        self.hasher = PasswordHash.recommended()

    def hash(self, plain: str) -> str:
        return self.hasher.hash(plain)

    def verify(self, plain: str, hashed: str) -> bool:
        return self.hasher.verify(plain, hashed)
