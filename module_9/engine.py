from sqlalchemy import create_engine

from module_9.settings import CONNECTION_STRING_MODULE_9
from module_9.settings import CONNECTION_STRING_CHINOOK

engine = create_engine(CONNECTION_STRING_MODULE_9, echo=True, pool_size=10, max_overflow=0)
engine_chinook = create_engine(CONNECTION_STRING_CHINOOK, echo=True)