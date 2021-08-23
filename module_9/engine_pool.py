from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool, NullPool, SingletonThreadPool

from module_9.settings import CONNECTION_STRING_CHINOOK as CONNECTION_STRING


# SQLite https://docs.sqlalchemy.org/en/14/core/pooling.html#connection-pool-configuration
engine = create_engine(CONNECTION_STRING, poolclass=QueuePool)