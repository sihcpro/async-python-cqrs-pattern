# System
ENV = "default"

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

# Extra path
DATABASE_PATH = "data/database"
