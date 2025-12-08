from dataclasses import dataclass
from datetime import datetime


@dataclass
class RefreshTokenDTO:
    jti: str
    user_id: str
    created_at: datetime
    expires_at: datetime
