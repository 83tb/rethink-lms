import sys
from kombu import Connection, Exchange

class NotificationEmiter(object):
    def __init__(self, amqp_address, exchange=None):
        self._connection = Connection(amqp_address)
        self._exchange = Exchange('topic_msg', 'topic', durable=True) if exchange is None else exchange

    def connect(self):
        self._connection.connect()

    def disconnect(self):
        self._connection.release()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def notify(self, topic, msg):
        with self._connection.channel() as ch:
            bound_ex = self._exchange(ch)
            bound_ex.declare()
            bound_ex.publish(bound_ex.Message(msg), routing_key=topic)


if __name__ == '__main__':
    topic = sys.argv[1] if len(sys.argv) > 1 else 'a'
    msg = ' '.join(sys.argv[2:]) or 'Hello world!'

    with NotificationEmiter('amqp://guest:guest@192.168.99.100:32769') as emiter:
        emiter.notify(topic, msg)
        print " [x] Sent %r:%r" % (topic, msg)
