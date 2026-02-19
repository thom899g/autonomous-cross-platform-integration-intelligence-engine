from typing import Dict, Any
import pika

class EventBus:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self, host: str, port: int) -> None:
        """Connect to the message broker (e.g., RabbitMQ)."""
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
            self.channel = self.connection.channel()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to event bus: {str(e)}")

    def publish(self, exchange_name: str, routing_key: str, message: Dict[str, Any]) -> None:
        """Publish events to the event bus."""
        try:
            self.channel.basic_publish(exchange=exchange_name,
                                      routing_key=routing_key,
                                      body=message)
        except Exception as e:
            raise PublishingError(f"Failed to publish event: {str(e)}")

    def subscribe(self, exchange_name: str, queue_name: str, callback) -> None:
        """Subscribe to events on the event bus."""
        try:
            self.channel.queue_declare(queue=queue_name)
            self.channel.basic_consume(queue=queue_name,
                                      on_message_callback=callback)
        except Exception as e:
            raise SubscriptionError(f"Failed to subscribe: {str(e)}")

    def disconnect(self) -> None:
        """Disconnect from the event bus."""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
        except Exception as e:
            raise DisconnectionError(f"Failed to close connection: {str(e)}