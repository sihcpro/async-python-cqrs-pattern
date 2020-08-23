# System
ENV = "default"

# Application
APP_SORT_NAME = "BAS"
APP_NAME = "Bridging All Space"
APP_HOST = "0.0.0.0"
APP_PORT = 8080

# DataBase
SCHEMA_NAME = "BAS"
DB_DSN = "postgres://postgres:postgres@localhost/local?sslmode=require"
DB_SSL = "require"

# Logger
LOG_LEVEL = "DEBUG"
LOG_FORMATTER = (
    "%(asctime)s [ %(name)-10s- %(module)-16s:%(lineno)4s] %(levelname)-7s: "
    "%(message)s"
)
LOG_DATEFMT = "%y-%m-%d %H:%M:%S"
LOG_OUTPUT = "stdout"
LOG_OUTPUT_SECONDARY = None

# Format
DATETIME_FMT = "%Y-%m-%d %H:%M:%S.%f"
DATE_FMT = "%Y-%m-%d"

# Validation
IGNORE_EXTRA_FIELDS = True

# Invironment
DEBUG = True
DEBUG_CORE = True
DEBUG_SQL = False
