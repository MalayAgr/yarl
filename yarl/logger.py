import logging

from logstash_async.transport import HttpTransport
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter

host = "localhost"
port = 50000

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


transport = HttpTransport(
    host,
    port,
    ssl_enable=False,
    ssl_verify=False,
    timeout=5.0,
)

handler = AsynchronousLogstashHandler(
    host, port, transport=transport, database_path="logstash_test.db"
)
formatter = LogstashFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
