from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select, update as sql_update, delete as sql_delete
from typing import Type, TypeVar, Generic, Optional, List
from Helpers.logger import get_logger

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model
        self.logger = get_logger(__class__.__name__)

    async def _commit(self):
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            self.logger.error(e, exc_info=True)
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            self.logger.error(e, exc_info=True)
            raise

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self._commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, id: int) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalars().first()

    async def get_all(self) -> List[T]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def filter(self, **kwargs) -> List[T]:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, id: int, data: dict) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = result.scalars().first()
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        await self._commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: int) -> bool:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = result.scalars().first()
        if not obj:
            return False
        await self.session.delete(obj)
        await self._commit()
        return True

    async def count(self) -> int:
        result = await self.session.execute(select(self.model))
        return len(result.scalars().all())

    async def exists(self, **kwargs) -> bool:
        result = await self.session.execute(
            select(self.model).filter_by(**kwargs)
        )
        return result.scalars().first() is not None
