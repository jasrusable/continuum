from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String, Integer, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, configure_mappers, relationship
from sqlalchemy_continuum import make_versioned


Base = declarative_base()

make_versioned(user_cls=None)


class Article(Base):
    __tablename__ = 'article'
    __versioned__ = {}

    id = Column(Integer, primary_key=True)
    categories = relationship(
        'Category',
        secondary='article_category',
        back_populates='articles',
    )
    author = Column(String)


class ArticleCategory(Base):
    __tablename__ = 'article_category'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    article_id = Column(Integer, ForeignKey('article.id'), nullable=False)


class Category(Base):
    __tablename__ = 'category'
    __versioned__ = {}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    articles = relationship(
        'Article',
        secondary='article_category',
        back_populates='categories',
    )


configure_mappers()

postgres = 'postgres://jason:123@localhost/test'
sqlite = 'sqlite://'

engine = create_engine(sqlite, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

a = Article(author='Jason')
c = Category(name='Some Category')
a.categories.append(c)
session.add(a)
session.commit()
