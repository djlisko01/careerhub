from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import settings


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from typing import Generator

from config import settings

# Engine: manages a pool of reusable database connections.
# Created once at module level so the pool is shared across all requests.
# If created per-request, you'd be spinning up a new pool every time (wasteful).
# pool_size = how many connections stay open; max_overflow = extra connections
# allowed under load; pool_timeout = seconds to wait for a connection before erroring.
Engine = create_engine(settings.postgres_url)

# Session factory: a template for creating sessions.
# autocommit=False: you control when commits happen (explicit db.commit()).
# autoflush=False: changes aren't sent to the DB until you explicitly flush/commit.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session.

    Returns:
        Generator[Session, None, None]: A generator that yields a SQLAlchemy Session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
