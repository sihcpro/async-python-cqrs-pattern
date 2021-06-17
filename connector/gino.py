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
    logger.info("DB_DSN: %r", config.DB_DSN)
    logger.info("Done Connector")


async def get_async_connection() -> Gino:
    db = Gino(bind=config.DB_DSN)
    return db.bind
    return await connect(config.DB_DSN)


def get_pool():
    pool = create_pool(dsn=config.DB_DSN)
    return pool


def __sif__():
    _bind: Connection = None
    _engine = None

    async def _get_bind():
        nonlocal _bind
        if _bind is None:
            _bind = await db.set_bind(
                config.DB_DSN,
                ssl=default_ssl(),
            )
        return _bind

    def _get_engine():
        nonlocal _engine
        if _engine is None:
            _engine = create_engine(config.DB_DSN, echo=False)
        return _engine

    return _get_bind, _get_engine


get_bind, get_engine = __sif__()


def get_connection():
    engine = get_engine()
    return engine.connect()
