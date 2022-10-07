from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string

from apps.kafka_util import consume_forever


class Command(BaseCommand):
    help = "Start consuming from the specified topic"

    def add_arguments(self, parser):
        parser.add_argument("topic", help="Name of topic.")
        parser.add_argument("action", help="Function to process a message as dotted string.")

    def handle(self, topic, action, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Setup action: {action}"))
        action = import_string(action)

        self.stdout.write(self.style.SUCCESS(f"Start consuming from {topic=}..."))
        try:
            consume_forever(topic, action)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS(f"Stop consuming from {topic=}..."))
