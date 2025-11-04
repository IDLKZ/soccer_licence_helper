"""
Data Transfer Objects for User
DTO для передачи данных пользователя между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDTO:
    """DTO для отображения пользователя (без пароля)"""
    id: int
    email: str
    phone: str
    username: str
    first_name: str
    last_name: Optional[str]
    patronymic: Optional[str]
    iin: Optional[str]
    position: Optional[str]
    image_url: Optional[str]
    role_id: Optional[int]
    is_active: bool
    verified: bool
    created_at: datetime
    updated_at: datetime
    full_name: Optional[str] = None
    short_name: Optional[str] = None