import asyncio
import gino
from asyncpg import create_pool
from asyncpg.connection import Connection, connect
from gino import Gino
from sqlalchemy.engine import create_engine

from base.model import db
from base.sanic import SanicApp
from base.ssl import default_ssl
from .cfg import config, logger


def config_connector(app: SanicApp):
    logger.info("Init Connector")
    # db = Gino(bind=config.DB_DSN)
    # asyncio.run()
    # app.engine = asyncio.run(gino.create_engine(config.DB_DSN, ssl="require"))
    # db.init_app(app)
    app.get_async_db_conn = get_async_connection
    app.get_db_conn = get_connection
    print("config.DB_DSN 1", config.DB_DSN)
    logger.info("Done Connector")


def get_connection():
    engine = create_engine(config.DB_DSN, echo=False)
    return engine.connect()


async def get_async_connection() -> Gino:
    db = Gino(bind=config.DB_DSN)
    return db.bind
    return await connect(config.DB_DSN)


def get_pool():
    pool = create_pool(dsn=config.DB_DSN)


def __sif__():
    _bind: Connection = None

    async def _get_bind():
        nonlocal _bind
        if _bind is None:
            print("config.DB_DSN 2", config.DB_DSN)
            _bind = await db.set_bind(
                config.DB_DSN,
                ssl=default_ssl(),
            )
        return _bind

    return _get_bind


get_bind = __sif__()
