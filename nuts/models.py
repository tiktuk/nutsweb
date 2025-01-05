from django.db import models
from django_extensions.db.models import TimeStampedModel


class Host(TimeStampedModel):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    social_links = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class Show(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    show_alias = models.CharField(max_length=255, unique=True)
    external_links = models.JSONField(default=list, blank=True)
    location_short = models.CharField(max_length=10, blank=True)
    location_long = models.CharField(max_length=255, blank=True)
    intensity = models.IntegerField(null=True, blank=True)
    hosts = models.ManyToManyField(Host, related_name="shows", blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value


class Mood(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value


class Episode(TimeStampedModel):
    STATUS_CHOICES = [
        ("published", "Published"),
        ("pending", "Pending"),
    ]

    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="episodes")
    broadcast_title = models.CharField(max_length=255)
    episode_alias = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()
    broadcast = models.DateTimeField()
    mixcloud_url = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    moods = models.ManyToManyField(Mood, blank=True)

    def __str__(self):
        return f"{self.broadcast_title} ({self.broadcast.date()})"

    class Meta:
        ordering = ["-broadcast"]


class AudioSource(TimeStampedModel):
    episode = models.ForeignKey(
        Episode, on_delete=models.CASCADE, related_name="audio_sources"
    )
    url = models.URLField()
    source = models.CharField(max_length=50)  # e.g., "soundcloud", "mixcloud"

    def __str__(self):
        return f"{self.source}: {self.url}"


class Media(TimeStampedModel):
    episode = models.OneToOneField(
        Episode, on_delete=models.CASCADE, related_name="media"
    )
    background_large = models.URLField()
    background_medium_large = models.URLField()
    background_medium = models.URLField()
    background_small = models.URLField()
    background_thumb = models.URLField()
    picture_large = models.URLField()
    picture_medium_large = models.URLField()
    picture_medium = models.URLField()
    picture_small = models.URLField()
    picture_thumb = models.URLField()

    def __str__(self):
        return f"Media for {self.episode}"


class Channel(TimeStampedModel):
    name = models.CharField(max_length=50)  # e.g., "1", "2"

    def __str__(self):
        return f"Channel {self.name}"


class Broadcast(TimeStampedModel):
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="broadcasts"
    )
    episode = models.ForeignKey(
        Episode, on_delete=models.CASCADE, related_name="broadcasts"
    )
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.channel} - {self.episode} ({self.start_timestamp})"

    class Meta:
        ordering = ["start_timestamp"]
