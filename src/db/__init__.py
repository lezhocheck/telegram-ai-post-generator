import contextlib
from sqlalchemy import create_engine, Connection
from typing import Iterator, Any
from sqlalchemy.orm import sessionmaker
from src.db.models import Base


class DbSessionManager:
    def __init__(self, host: str, **engine_kwargs: Any) -> None:
        self._engine = create_engine(host, **engine_kwargs)
        self._sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    def close(self) -> None:
        self._assert_initialized()
        self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.contextmanager
    def session(self) -> Iterator[Connection]:
        self._assert_initialized()
        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_tables(self) -> None:
        self._assert_initialized()
        Base.metadata.create_all(self._engine)
    
    def drop_tables(self) -> None:
        self._assert_initialized()
        Base.metadata.drop_all(self._engine)

    def _assert_initialized(self) -> None:
        if self._engine is None or self._sessionmaker is None:
            raise Exception(f'{self.__class__} is not initialized')
        