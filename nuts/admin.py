from django.contrib import admin
from .models import Show, Genre, Mood, Episode, AudioSource, Media, Channel, Broadcast, Host


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]
    search_fields = ["name", "bio"]


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ["name", "show_alias", "location_long", "created"]
    search_fields = ["name", "show_alias", "description"]
    list_filter = ["location_short"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "value"]
    search_fields = ["id", "value"]


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ["id", "value"]
    search_fields = ["id", "value"]


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ["broadcast_title", "show", "broadcast", "status"]
    list_filter = ["status", "show", "broadcast"]
    search_fields = ["broadcast_title", "episode_alias"]
    date_hierarchy = "broadcast"


@admin.register(AudioSource)
class AudioSourceAdmin(admin.ModelAdmin):
    list_display = ["episode", "source", "url"]
    list_filter = ["source"]
    search_fields = ["url"]


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ["episode", "created"]
    search_fields = ["episode__broadcast_title"]


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ["channel", "episode", "start_timestamp", "end_timestamp"]
    list_filter = ["channel"]
    date_hierarchy = "start_timestamp"
    search_fields = ["episode__broadcast_title"]
