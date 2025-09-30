class MQException(Exception):
    pass


class MQConnectionException(MQException):
    pass


class MQPublishException(MQException):
    pass


class SyncQueueException(Exception):
    pass
