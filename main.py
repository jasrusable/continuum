import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_continuum import make_versioned


Base = declarative_base()

make_versioned(user_cls=None)


class Article(Base):
    __versioned__ = {}
    __tablename__ = 'article'

    id = sa.Column(sa.Integer, primary_key=True)


sa.orm.configure_mappers()

engine = create_engine('sqlite:///db.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


# after you have defined all your models, call configure_mappers:

Base.metadata.create_all(engine)
