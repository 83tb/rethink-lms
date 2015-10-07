import sys
from kombu import Connection, Exchange, Queue

class NotificationReceiver(object):
    def __init__(self, amqp_address, queue, exchange=None):
        self._connection = Connection(amqp_address)
        self._exchange = Exchange('topic_msg', 'topic', durable=True) if exchange is None else exchange
        self._queue = queue
        self._callbacks = []
        self._topics = []

    def connect(self):
        self._connection.connect()

    def disconnect(self):
        self._connection.release()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def register_callback(self, callback):
        self._callbacks.append(callback)

    def subscribe(self, topics):
        if isinstance(topics, list):
            self._topics.extend(topics)
        else:
            self._topics.append(topics)

    def listen(self):
        with self._connection.channel() as ch:
            bound_ex = self._exchange(ch)
            bound_ex.declare()
            bound_q = self._queue(ch)
            bound_q.declare()
            for topic in self._topics:
                bound_q.bind_to(bound_ex, routing_key=topic, nowait=True)

            with self._connection.Consumer(bound_q, callbacks=self._callbacks):
                while True:
                    self._connection.drain_events()


if __name__ == '__main__':
    def cb(body, msg):
        print " [x] {}:{}".format(msg.delivery_info['routing_key'], msg.body)
        msg.ack()

    if len(sys.argv) < 2:
        print >> sys.stderr, "Usage: {} queue_name (topic)+".format(sys.argv[0])
        sys.exit(1)

    queue_name = sys.argv[1]
    topics = sys.argv[2:]

    q = Queue(name=queue_name)
    recv = NotificationReceiver('amqp://guest:guest@192.168.99.100:32769', q)
    recv.subscribe(topics)
    recv.register_callback(cb)
    with recv:
        print ' [*] Waiting for logs...'
        recv.listen()
