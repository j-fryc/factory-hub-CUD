from enum import Enum
from typing import Union

import pika
from pika.exceptions import (
    AMQPConnectionError,
    AMQPChannelError,
    ChannelClosedByBroker,
    ConnectionClosedByBroker,
    NackError,
    UnroutableError,
    StreamLostError,
    AMQPError
)

from app.db_sync.exceptions import MQPublishException, MQException, MQConnectionException


class ExchangeType(Enum):
    DIRECT = 'direct'
    FANOUT = 'fanout'
    TOPIC = 'topic'
    HEADERS = 'headers'


class MQProducer:
    def __init__(
            self,
            exchange_type: ExchangeType = ExchangeType.DIRECT,
            exchange_name: str = 'db_sync',
            host: str = 'rabbit-mq',
            port: int = 5672,
            user: str = 'user',
            password: str = 'pass'
    ):
        self._exchange_type = exchange_type
        self._exchange_name = exchange_name
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._connection = None
        self._channel = None

    def publish_data(self, msg: Union[bytes, str], routing_key: str) -> None:
        if not isinstance(msg, (bytes, str)):
            raise TypeError("Message must be bytes or str.")
        if isinstance(msg, str):
            msg = msg.encode('utf-8')

        try:
            self._channel.basic_publish(
                exchange=self._exchange_name,
                routing_key=routing_key,
                body=msg,
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
                ),
                mandatory=True
            )
        except NackError as e:
            raise MQPublishException(f"Message was rejected by broker: {e}")
        except UnroutableError as e:
            raise MQPublishException(f"Message could not be routed: {e}")
        except (ChannelClosedByBroker, AMQPChannelError) as e:
            raise MQPublishException(f"Channel error during publish: {e}")
        except (ConnectionClosedByBroker, AMQPConnectionError, StreamLostError) as e:
            raise MQConnectionException(f"Connection error during publish: {e}")
        except AMQPError as e:
            raise MQException(f"AMQP error during publish: {e}")
        except Exception as e:
            raise MQException(f"Unexpected error during publish: {e}")

    def __enter__(self):
        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self._host,
                    port=self._port,
                    credentials=pika.PlainCredentials(
                        username=self._user,
                        password=self._password
                    )
                )
            )
            self._channel = self._connection.channel()
            self._channel.exchange_declare(
                exchange=self._exchange_name,
                exchange_type=self._exchange_type.value
            )
            self._channel.confirm_delivery()
        except (AMQPConnectionError, ConnectionClosedByBroker, StreamLostError) as e:
            raise MQConnectionException(f"Failed to connect to RabbitMQ: {e}")
        except Exception as e:
            raise MQConnectionException(f"Unexpected error connecting to RabbitMQ: {e}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self._channel and self._channel.is_open:
                self._channel.close()
            if self._connection and self._connection.is_open:
                self._connection.close()
        except Exception:
            pass


def get_mq_producer():
    return MQProducer()
