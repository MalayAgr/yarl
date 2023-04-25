import logging
import os

from dotenv import dotenv_values
from logstash_async.formatter import LogstashFormatter  # type: ignore
from logstash_async.handler import AsynchronousLogstashHandler  # type: ignore
from logstash_async.transport import HttpTransport  # type: ignore


def get_env():
    parent = os.path.dirname(__file__)
    path = os.path.join(parent, "assets", ".env")
    return dotenv_values(dotenv_path=path)


env = get_env()

PRODUCTION = env.get("PRODUCTION", "False") == "True"

logger = logging.getLogger(__name__)


if PRODUCTION:
    host = env.get("LOGGER_HOST", "localhost")
    port = int(env.get("LOGGER_PORT", 5000))  # type: ignore

    logger.setLevel(logging.INFO)

    transport = HttpTransport(
        host,  # type: ignore
        port,
        ssl_enable=False,
        ssl_verify=False,
        timeout=5.0,
    )

    handler = AsynchronousLogstashHandler(
        host, port, transport=transport, database_path="logstash_test.db"  # type: ignore
    )
    formatter = LogstashFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
else:
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("development.log")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
