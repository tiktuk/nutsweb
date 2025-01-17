from typing import List
from ninja import NinjaAPI, ModelSchema
from django.shortcuts import get_object_or_404
from .models import Broadcast, Episode, Show, Host, Channel

api = NinjaAPI(version="1.0")

# Schemas
class ChannelSchema(ModelSchema):
    class Config:
        model = Channel
        model_fields = ["id", "name"]

class HostSchema(ModelSchema):
    class Config:
        model = Host
        model_fields = ["id", "name", "bio", "image_url", "social_links"]

class ShowSchema(ModelSchema):
    hosts: List[HostSchema]

    class Config:
        model = Show
        model_fields = ["id", "name", "description", "show_alias", "external_links", 
                       "location_short", "location_long", "intensity"]

class EpisodeSchema(ModelSchema):
    show: ShowSchema

    class Config:
        model = Episode
        model_fields = ["id", "broadcast_title", "episode_alias", "status", 
                       "start_timestamp", "end_timestamp", "broadcast", "mixcloud_url"]

class BroadcastSchema(ModelSchema):
    episode: EpisodeSchema
    channel: ChannelSchema

    class Config:
        model = Broadcast
        model_fields = ["id", "start_timestamp", "end_timestamp"]

# Endpoints
@api.get("/broadcasts", response=List[BroadcastSchema])
def list_broadcasts(request):
    return Broadcast.objects.select_related("episode", "episode__show", "channel").all()

@api.get("/broadcasts/{broadcast_id}", response=BroadcastSchema)
def get_broadcast(request, broadcast_id: int):
    return get_object_or_404(Broadcast.objects.select_related("episode", "episode__show", "channel"), id=broadcast_id)

@api.get("/episodes", response=List[EpisodeSchema])
def list_episodes(request):
    return Episode.objects.select_related("show").prefetch_related("show__hosts").all()

@api.get("/episodes/{episode_id}", response=EpisodeSchema)
def get_episode(request, episode_id: int):
    return get_object_or_404(Episode.objects.select_related("show").prefetch_related("show__hosts"), id=episode_id)

@api.get("/shows", response=List[ShowSchema])
def list_shows(request):
    return Show.objects.prefetch_related("hosts").all()

@api.get("/shows/{show_id}", response=ShowSchema)
def get_show(request, show_id: int):
    return get_object_or_404(Show.objects.prefetch_related("hosts"), id=show_id)

@api.get("/hosts", response=List[HostSchema])
def list_hosts(request):
    return Host.objects.all()

@api.get("/hosts/{host_id}", response=HostSchema)
def get_host(request, host_id: int):
    return get_object_or_404(Host, id=host_id)
