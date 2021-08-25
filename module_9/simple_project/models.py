from sqlalchemy import Table, Column, Integer, String, MetaData, Unicode
metadata = MetaData()

user = Table(
    'app_user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', Unicode(50)),
    Column('last_name', Unicode(50)),
    Column('address', Unicode(200)),
    Column('email', String(50), nullable=False),
    # Column('phone', String(50)),
)