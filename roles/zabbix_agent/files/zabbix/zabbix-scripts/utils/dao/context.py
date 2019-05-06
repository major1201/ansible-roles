# encoding= utf-8
from __future__ import division, absolute_import, with_statement, print_function
from utils import strings, logger

DAO_LOGGER = 'DAO'


class DBConfig(object):
    DEFAULT_POOL_SIZE = 20
    DEFAULT_MAX_OVERFLOW = 0
    DEFAULT_POOL_RECYCLE = 5
    DEFAULT_POOL_TIMEOUT = 3600

    @classmethod
    def from_dict(cls, _dict):
        assert isinstance(_dict, dict)
        if 'url' not in _dict:
            raise ValueError('The "_dict" should contain the "url" key.')
        return DBConfig(
            url=_dict.get('url'),
            pool_size=_dict.get('pool_size', DBConfig.DEFAULT_POOL_SIZE),
            max_overflow=_dict.get('pool_size', DBConfig.DEFAULT_MAX_OVERFLOW),
            pool_recycle=_dict.get('pool_size', DBConfig.DEFAULT_POOL_RECYCLE),
            pool_timeout=_dict.get('pool_size', DBConfig.DEFAULT_POOL_TIMEOUT),
        )

    def __init__(self, url, pool_size=DEFAULT_POOL_SIZE, max_overflow=DEFAULT_MAX_OVERFLOW, pool_recycle=DEFAULT_POOL_RECYCLE, pool_timeout=DEFAULT_POOL_TIMEOUT):
        self._url = url
        self._pool_size = pool_size
        self._max_overflow = max_overflow
        self._pool_recycle = pool_recycle
        self._pool_timeout = pool_timeout

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def pool_size(self):
        return self._pool_size

    @pool_size.setter
    def pool_size(self, pool_size):
        self._pool_size = pool_size

    @property
    def max_overflow(self):
        return self._max_overflow

    @max_overflow.setter
    def max_overflow(self, max_overflow):
        self._max_overflow = max_overflow

    @property
    def pool_recycle(self):
        return self._pool_recycle

    @pool_recycle.setter
    def pool_recycle(self, pool_recycle):
        self._pool_recycle = pool_recycle

    @property
    def pool_timeout(self):
        return self._pool_timeout

    @pool_timeout.setter
    def pool_timeout(self, pool_timeout):
        self._pool_timeout = pool_timeout


class DBContext:
    _tl = None
    _metadata = None
    _DBSession = None
    has_initialized = False

    @classmethod
    def initialize(cls, db_config):
        import threading
        import pymysql
        from sqlalchemy import create_engine, MetaData
        from sqlalchemy.orm import sessionmaker

        logger.info('INITIALIZING', DAO_LOGGER)

        pymysql.install_as_MySQLdb()
        cls._tl = threading.local()

        assert isinstance(db_config, DBConfig)
        engine = create_engine(db_config.url, pool_size=db_config.pool_size, max_overflow=db_config.max_overflow,
                               pool_recycle=db_config.pool_recycle, pool_timeout=db_config.pool_timeout, echo=False)
        cls._metadata = MetaData(engine)
        cls._DBSession = sessionmaker(bind=engine, autoflush=False)

        cls.has_initialized = True

        logger.info('INITIALIZING OK', DAO_LOGGER)

    def __init__(self):
        if not DBContext.has_initialized:
            raise Exception('DBContext has not been initialized, please call DBContext.initialze(db_config).')
        if (not hasattr(DBContext._tl, 'session')) or (DBContext._tl.session is None):
            DBContext._tl.session = DBContext._DBSession()
        self.session = DBContext._tl.session
        self.nest_level = 0

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        return False

    def begin(self):
        if self.nest_level == 0:
            logger.debug('BEGIN', DAO_LOGGER)
        self.nest_level += 1

    def commit(self):
        if self.nest_level <= 0:
            raise Exception("session is closed.")
        self.nest_level -= 1
        if self.nest_level == 0:
            try:
                self.session.flush()
                self.session.commit()
                logger.debug('COMMIT', DAO_LOGGER)
            except Exception:
                self.rollback()
            finally:
                self.close()

    def rollback(self):
        try:
            self.session.rollback()
            logger.debug('ROLLBACK', DAO_LOGGER)
        except IOError:
            pass
        finally:
            self.nest_level = 0
            self.close()

    def close(self):
        try:
            self.session.close()
        except IOError as e:
            logger.error_traceback(DAO_LOGGER)

    def execute_delete(self, table_name, where_clause, **params):
        sql = "delete from " + table_name + " where " + where_clause
        self.execute(sql, **params)

    def execute(self, sql, **params):
        from sqlalchemy import text

        try:
            self.begin()
            self.session.connection().execute(text(sql), **params)
            logger.debug(str(sql), DAO_LOGGER)
            logger.debug(strings.to_json(params), DAO_LOGGER)
            self.commit()
        except Exception as e:
            self.rollback()
            raise e

    def create_query(self, table_name, where_clause, **params):
        from utils.dao.query import DaoQuery

        sql = "select * from " + table_name + " where " + where_clause
        return DaoQuery(self, sql, **params)

    def create_sql_query(self, sql, **params):
        from utils.dao.query import DaoQuery

        return DaoQuery(self, sql, **params)

    def save(self, table_name, obj):
        assert isinstance(obj, dict)
        if ("id" not in obj) or strings.is_blank(obj["id"]):
            obj["id"] = strings.uuid()
            insert_flag = True
        else:
            count = self.create_sql_query("select count(id) c from " + table_name + " where id = :id",
                                          id=obj["id"]).fetch()[0]["c"]
            insert_flag = int(count) == 0
        if insert_flag:
            arr = ["insert into", table_name, "(", ",".join(obj.keys()), ") values(",
                   ",".join([":" + k for k in obj.keys()]), ")"]
        else:
            arr = ["update", table_name, "set", ",".join([k + "=:" + k for k in obj.keys()]), "where id=:id"]
        try:
            self.begin()
            self.execute(" ".join(arr), **obj)
            self.commit()
        except Exception as e:
            self.rollback()
            raise e

    def delete(self, table_name, obj):
        assert isinstance(obj, dict)
        if ("id" in obj) and strings.is_not_blank(obj["id"]):
            self.delete_byid(table_name, obj["id"])

    def delete_byid(self, table_name, oid):
        oid = strings.strip_to_empty(oid)
        self.execute_delete(table_name, "id=:id", id=oid)

    def get(self, table_name, oid):
        res = self.create_query(table_name, "id=:id", id=oid).fetch()
        if len(res) > 0:
            return res[0]
        return None
