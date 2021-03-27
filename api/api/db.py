from flask import current_app, g
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DateTime, Enum

#THIS IS BS PLACEHOLDER COPIED RANDOMLY FROM DOC. DON'T USE IT IDIOT


def init_db():
    if 'db' not in g:
        engine = create_engine(current_app.config['POSTGRES_DB_URL'], echo=True)
        g.db = engine


metadata = MetaData()
signup = Table('signups', metadata,
               Column('id', Integer, primary_key=True),
               Column('first_name', String, nullable=False),
               Column('last_name', String, nullable=False),
               Column('email', String, nullable=False),
               Column('signup_uuid', String, nullable=False),
               Column('created_at', DateTime))