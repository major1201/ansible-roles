# encoding: utf-8
from __future__ import division, absolute_import, with_statement, print_function
from utils import strings, logger
from utils.dao.context import DAO_LOGGER
from sqlalchemy import text


class DaoQuery:
    def __init__(self, context, sql, **params):
        self._context = context
        self._sql = sql
        self._params = params
        self._order_by_clause = ""
        self._start = 0
        self._fetch_rows = -1  # not limited

    def fetch(self, raw=False):
        if raw:
            sql_arr = [self._sql]
        else:
            sql_arr = ["select _page.* from (", self._sql, ") _page"]
            if strings.is_not_blank(self._order_by_clause):
                sql_arr.append("order by")
                sql_arr.append(self._order_by_clause)
            if self._fetch_rows >= 0:
                sql_arr.append("limit " + str(self._start) + "," + str(self._fetch_rows))

        try:
            self._context.begin()
            cursor = self._build_cursor_sql(" ".join(sql_arr))
            fetchall = cursor.fetchall()
            logger.debug(" ".join(sql_arr), DAO_LOGGER)
            logger.debug(strings.to_json(self._params), DAO_LOGGER)
            self._context.commit()
            return list(map(lambda o: dict(zip([k.lower() for k in cursor.keys()], o)), fetchall))
        except Exception as e:
            self._context.rollback()
            raise e

    def first(self):
        try:
            self._context.begin()
            cursor = self._build_cursor()
            first = cursor.first()
            logger.debug('FIRST ' + str(self._sql), DAO_LOGGER)
            logger.debug(strings.to_json(self._params), DAO_LOGGER)
            keys = cursor.keys()
            self._context.commit()
            return None if first is None else dict(zip([o.lower() for o in keys], first))
        except Exception as e:
            self._context.rollback()
            raise e

    def count(self):
        try:
            self._context.begin()
            count = 0
            sql_arr = ["select count(*) from (", self._sql, ") _count"]
            result = self._build_cursor_sql("".join(sql_arr)).fetchall()
            logger.debug(''.join(sql_arr), DAO_LOGGER)
            logger.debug(strings.to_json(self._params), DAO_LOGGER)
            if len(result) > 0:
                count = result[0][0]
            self._context.commit()
            return count
        except Exception as e:
            self._context.rollback()
            raise e

    def order_by(self, exp):
        self._order_by_clause = exp
        return self

    def pagination(self, start, fetch_rows):
        self._start = start
        self._fetch_rows = fetch_rows
        return self

    def _build_cursor(self):
        return self._context.session.connection().execute(text(self._sql), **self._params)

    def _build_cursor_sql(self, sql):
        return self._context.session.connection().execute(text(sql), **self._params)
