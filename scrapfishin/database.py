from contextlib import contextmanager
from typing import Tuple
import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, scoped_session, Session
import sqlalchemy as sa


Base = declarative_base()
log = logging.getLogger(__name__)


class Database:
    def __init__(self, conn_string: str):
        self._engine = sa.create_engine(conn_string)
        self._session_factory = sessionmaker(bind=self._engine)
        self._Session = scoped_session(self._session_factory)

    @property
    def engine(self):
        return self._engine

    @contextmanager
    def session(self, **kwargs) -> Session:
        """
        Handles all the messy details of session work.
        """
        self._session = sess = self._Session(**kwargs)

        try:
            yield sess
            sess.commit()
        except Exception as e:
            sess.rollback()
            log.exception(f'{type(e).__name__}: {e}')
            # raise e
        finally:
            sess.close()
            self._session = None

    def __repr__(self):
        return f'<Database {self._engine.url}>'


def get_or_create(
    session: Session,
    model: declarative_base,
    **data
) -> Tuple[declarative_base, bool]:
    """
    Implementation of GET/CREATE <model(**kwargs)>.

    If the data already exists in the database, simply return the model.
    Otherwise, we create and add it to the database, then return it.

    Parameters
    ----------
    session : sqlalchemy.orm.session.Session
        sqlalchemy session to use for this transaction

    model : sqlalchemy.ext.declarative.declarative_base
        sqlalchemy model to fill with data

    **data
        fields and values to feed into the model

    Returns
    -------
    (model, created)
        record retrieved from the database
        whether or not the record was created
    """
    try:
        return session.query(model).filter_by(**data).one(), True
    except NoResultFound:
        try:
            with session.begin_nested():
                created = model(**data)
                session.add(created)
            return created, False
        except sa.exc.IntegrityError:
            return session.query(model).filter_by(**data).one(), True
