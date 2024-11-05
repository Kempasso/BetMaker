import typing

from sqlalchemy import BooleanClauseList, select, asc, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload

ModelType = typing.TypeVar(name="ModelType", bound=typing.Any)

# TODO: Make dict like whereclause later
class DBStorage(typing.Generic[ModelType]):
    def __init__(self, model_cls: type[ModelType], session: AsyncSession):
        self.model_cls = model_cls
        self.session = session

    async def add(
        self,
        *,
        item: ModelType | None = None,
        items: list[ModelType] | None = None
    ) -> None:
        if item is not None:
            self.session.add(item)
        elif items is not None:
            self.session.add_all(items)
        else:
            raise ValueError(
                "There is no methods which accept `None` as argument"
            )
        await self.session.flush()

    async def get(
        self,
        where: BooleanClauseList = None,
        order_by: str = None,
        ascending: bool = True,
        limit: int = None,
        offset: int = None,
        load: tuple[str | InstrumentedAttribute] = None
    ) -> list[ModelType]:
        options = [
            selectinload(
                getattr(self.model_cls, col) if isinstance(col, str) else col
            )
            for col in (load or [])
        ]
        query = select(self.model_cls).options(*options)

        if where is not None:
            query = query.where(where)

        if order_by:
            col = (
                getattr(self.model_cls, order_by)
                if isinstance(order_by, str) else order_by
            )
            query = query.order_by(asc(col) if ascending else desc(col))
        cursor = await self.session.execute(query.limit(limit).offset(offset))
        return cursor.scalars().all()

    async def create(self, **values) -> ModelType | None:
        item = self.model_cls(**values)
        await self.add(item=item)
        return item

    async def update(
        self,
        *items: ModelType,
        where: BooleanClauseList | dict | None = None,
        **values
    ) -> None:
        if not (items or where or values):
            raise ValueError(
                "There is no methods which accepts no arguments"
            )

        if where is not None:
            stmt = update(self.model_cls).where(where).values(**values)
            await self.session.execute(stmt)
        elif items:
            for item in items:
                for key, val in values.items():
                    setattr(item, key, val)
            await self.add(items=items)