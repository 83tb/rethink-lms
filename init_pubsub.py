from pubsub.notification_emiter import NotificationEmiter
from pubsub.notification_rec import NotificationReceiver

amqp_address = "amqp://guest:guest@192.168.99.100:32769"

class PubSub(object):
    def __init__(self):
        self.receiver = NotificationReceiver(amqp_address)
        self.emitter = NotificationEmiter(amqp_address)
