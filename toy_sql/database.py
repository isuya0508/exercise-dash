from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_path = Path(__file__).with_name('data') / 'db.sqlite'


@contextmanager
def session_scope(engine):
    """DB操作のトランザクションスコープを与える

    参照: https://docs.sqlalchemy.org/en/13/orm/session_basics.html

    Parameters
    ----------
    engine : sqlalchemy.engine.base.Engine

    Yields
    -------
    session : sqlalchemy.orm.session.Session
    """

    session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except BaseException as e:
        session.rollback()
        raise e
    finally:
        session.close()


# mypyのtypeチェックにBaseを適応するとエラーになる。
# Baseは動的クラスなので、静的な型のチェックができないため。
# そのため、Baseを継承させたクラスを定義するとき「type: ignore」を指定してチェックを回避する。
# 参照: https://github.com/python/mypy/issues/6372
Base = declarative_base()


class Country(Base):  # type: ignore
    __tablename__ = 'country'

    name = Column(String, primary_key=True)
    landmass_id = Column(Integer, nullable=False)
    zone_id = Column(Integer, nullable=False)
    area = Column(Integer, nullable=False)
    population = Column(Integer, nullable=False)
    language_id = Column(Integer, nullable=False)
    religion_id = Column(Integer, nullable=False)


class Landmass(Base):  # type: ignore
    __tablename__ = 'landmass'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Zone(Base):  # type: ignore
    __tablename__ = 'zone'

    id = Column(Integer, primary_key=True)
    quadrant = Column(String, nullable=False)


class Language(Base):  # type: ignore
    __tablename__ = 'language'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Religion(Base):  # type: ignore
    __tablename__ = 'religion'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


def create_db(engine):
    """DBをengineに与えられたパスに生成する

    Parameters
    ----------
    engine : sqlalchemy.engine.base.Engine
    """
    Base.metadata.create_all(engine)
