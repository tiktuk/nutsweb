from django.core.management.base import BaseCommand
from django.utils import timezone
from nuts.models import Broadcast
from datetime import datetime


class Command(BaseCommand):
    help = "Lists all broadcasts ordered by time with day markers"

    def add_arguments(self, parser):
        parser.add_argument(
            "--channel",
            type=int,
            choices=[1, 2],
            help="Filter broadcasts by channel number (1 or 2)",
        )

    def handle(self, *args, **options):
        queryset = Broadcast.objects.select_related("episode", "channel")

        if options["channel"]:
            queryset = queryset.filter(channel__name=str(options["channel"]))

        broadcasts = queryset.order_by("start_timestamp")

        current_date = None

        for broadcast in broadcasts:
            broadcast_date = broadcast.start_timestamp.date()
            
            # Add day marker if we're on a new day
            if current_date != broadcast_date:
                current_date = broadcast_date
                self.stdout.write(
                    self.style.NOTICE(f"\n=== {current_date.strftime('%A, %B %d, %Y')} ===\n")
                )
            
            # Format and display broadcast info
            start_time = broadcast.start_timestamp.strftime("%H:%M")
            end_time = broadcast.end_timestamp.strftime("%H:%M")
            
            self.stdout.write(
                f"{start_time}-{end_time} | "
                f"{broadcast.channel.name} | "
                f"{broadcast.episode.broadcast_title}"
            )
