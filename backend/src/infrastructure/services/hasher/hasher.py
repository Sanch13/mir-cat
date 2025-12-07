from pwdlib import PasswordHash

from src.core.tracing import traced
from src.domain.user.interfaces import IPasswordHasher


class PasswordHasherImpl(IPasswordHasher):
    def __init__(self) -> None:
        self.hasher = PasswordHash.recommended()

    @traced(name="hashing_password")
    def hash(self, plain: str) -> str:
        return self.hasher.hash(plain)

    @traced(name="verify_password")
    def verify(self, plain: str, hashed: str) -> bool:
        return self.hasher.verify(plain, hashed)
