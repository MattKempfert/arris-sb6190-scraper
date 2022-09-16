from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from setting import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL, get_logger

logger = get_logger(name=__name__)


def connect():
    return InfluxDBClient(
        url=INFLUXDB_URL,
        token=INFLUXDB_TOKEN,
        org=INFLUXDB_ORG
    )


def format(value):
    suffixes = ['QAM', ' MHz', ' dBmV', ' dB', ' kSym/s']
    for suffix in suffixes:
        if value.endswith(suffix):
            value = value.removesuffix(suffix)

    try:
        # Should have put more effort in to break out an int vs a float but meh, convert all values to floats
        value = float(value)
    except ValueError:
        # A ValueError _should_ mean the value is an actual string and should not be converted to a float
        return value
    return value


def send_metrics(tags, fields):
    client = connect()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point("Arris SURFboard SB6190")

    for key, val in tags.items():
        point.tag(key, val)

    for key, val in fields.items():
        point.field(key, format(val))

    write_api.write(
        bucket=INFLUXDB_BUCKET,
        record=point
    )
