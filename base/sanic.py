from gino.engine import Connection, Engine
from sanic import Sanic


class SanicApp(Sanic):
    engine: Engine
    get_async_db_conn: Connection
    get_db_conn: Connection
