"""
Base Repository Implementation
Базовая реализация репозитория с общей функциональностью
"""
from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

T = TypeVar('T')
ModelType = TypeVar('ModelType')


class BaseRepository(Generic[ModelType]):
    """Базовый репозиторий с общей функциональностью"""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        """
        Инициализация репозитория

        Args:
            model: SQLAlchemy модель
            session: Асинхронная сессия
        """
        self.model = model
        self.session = session

    async def get_by_id(
        self,
        id: int,
        relationships: Optional[List[Any]] = None
    ) -> Optional[ModelType]:
        """
        Получить запись по ID

        Args:
            id: ID записи
            relationships: Список relationships для загрузки

        Returns:
            Модель или None
        """
        query = select(self.model).where(self.model.id == id)

        if relationships:
            for rel in relationships:
                query = query.options(selectinload(rel))

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        relationships: Optional[List[Any]] = None
    ) -> List[ModelType]:
        """
        Получить все записи

        Args:
            skip: Пропустить записи
            limit: Лимит записей
            relationships: Список relationships для загрузки

        Returns:
            Список моделей
        """
        query = select(self.model).offset(skip).limit(limit)

        if relationships:
            for rel in relationships:
                query = query.options(selectinload(rel))

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, obj: ModelType) -> ModelType:
        """
        Создать новую запись

        Args:
            obj: Объект модели

        Returns:
            Созданная модель
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: ModelType) -> ModelType:
        """
        Обновить запись

        Args:
            obj: Объект модели

        Returns:
            Обновленная модель
        """
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: ModelType) -> None:
        """
        Удалить запись

        Args:
            obj: Объект модели
        """
        await self.session.delete(obj)
        await self.session.commit()
