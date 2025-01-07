from django.core.management.base import BaseCommand
from datetime import datetime
from nutstosoup import (
    get_current_broadcasts,
    NTSAPIError,
    NTSAPITimeoutError,
    NTSAPIResponseError,
)
from nuts.models import Channel, Show, Episode, Broadcast, Media


class Command(BaseCommand):
    help = "Fetches current broadcasts from NTS API and stores them in the database"

    def handle(self, *args, **options):
        try:
            broadcasts = get_current_broadcasts()

            for broadcast in broadcasts:
                # Get or create channel
                channel, _ = Channel.objects.get_or_create(name=broadcast.channel)

                # Get or create show if we have show data
                show = None
                if broadcast.show_alias:
                    show, _ = Show.objects.get_or_create(
                        show_alias=broadcast.show_alias,
                        defaults={
                            "name": broadcast.name or "",
                            "description": broadcast.description or "",
                            "location_short": broadcast.location_short or "",
                            "location_long": broadcast.location_long or "",
                        },
                    )

                # Create episode
                start_time = datetime.fromisoformat(
                    broadcast.start_time.replace("Z", "+00:00")
                )
                end_time = datetime.fromisoformat(
                    broadcast.end_time.replace("Z", "+00:00")
                )

                if broadcast.episode_alias:
                    episode, _ = Episode.objects.get_or_create(
                        episode_alias=broadcast.episode_alias,
                        defaults={
                            "show": show,
                            "broadcast_title": broadcast.title,
                            "start_timestamp": start_time,
                            "end_timestamp": end_time,
                            "broadcast": start_time,
                            "status": "published",
                        },
                    )

                    # Create media if we have picture URL
                    if broadcast.picture_url and episode:
                        Media.objects.get_or_create(
                            episode=episode,
                            defaults={
                                "picture_large": broadcast.picture_url,
                                "picture_medium_large": broadcast.picture_url,
                                "picture_medium": broadcast.picture_url,
                                "picture_small": broadcast.picture_url,
                                "picture_thumb": broadcast.picture_url,
                                "background_large": broadcast.picture_url,
                                "background_medium_large": broadcast.picture_url,
                                "background_medium": broadcast.picture_url,
                                "background_small": broadcast.picture_url,
                                "background_thumb": broadcast.picture_url,
                            },
                        )

                    # Create broadcast
                    broadcast_obj, created = Broadcast.objects.get_or_create(
                        channel=channel,
                        episode=episode,
                        start_timestamp=start_time,
                        end_timestamp=end_time,
                    )

                    status = "Created" if created else "Updated"
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{status} broadcast: Channel {channel.name} - {episode.broadcast_title}"
                        )
                    )

        except NTSAPITimeoutError:
            self.stdout.write(self.style.ERROR("Request timed out"))
        except NTSAPIResponseError as e:
            self.stdout.write(self.style.ERROR(f"API error {e.status_code}: {str(e)}"))
        except NTSAPIError as e:
            self.stdout.write(self.style.ERROR(f"API error: {str(e)}"))
