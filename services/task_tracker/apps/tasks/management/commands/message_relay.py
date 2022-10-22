import logging
from time import sleep

from django.core.management import BaseCommand
from kafka_util import producer

from apps.tasks.models import OutboxTable

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Message Relay"

    def add_arguments(self, parser):
        parser.add_argument(
            "-i",
            "--interval",
            type=int,
            default=3,
            help="Interval in seconds",
        )

    def handle(self, interval: int, *args, **options):
        try:
            while True:
                for record in OutboxTable.objects.filter(sent=False).order_by("created_at"):
                    if producer.send_event(record.topic, record.payload, record.event_name, record.version):
                        record.sent = True
                        record.save(update_fields=["sent", "updated_at"])
                        logger.debug(f"{record=} successfully sent")
                sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("Shutting down..."))
