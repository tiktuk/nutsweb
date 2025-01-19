# NTS Web API Documentation

This document describes the REST API endpoints available in the NTS Web application.

## Base URL

The API is available at `/api/v1.0/` (e.g. `http://localhost:8000/api/v1.0/`) with all responses in JSON format.

## Endpoints

### Broadcasts

#### List all broadcasts
```http
GET /api/v1.0/broadcasts
```

Returns a list of all broadcasts with their associated episodes, shows, and channels.

#### Get a specific broadcast
```http
GET /api/v1.0/broadcasts/{broadcast_id}
```

Returns details for a specific broadcast by ID.

### Episodes

#### List all episodes
```http
GET /api/v1.0/episodes
```

Returns a list of all episodes with their associated shows and hosts.

#### Get a specific episode
```http
GET /api/v1.0/episodes/{episode_id}
```

Returns details for a specific episode by ID.

### Shows

#### List all shows
```http
GET /api/v1.0/shows
```

Returns a list of all shows with their associated hosts.

#### Get a specific show
```http
GET /api/v1.0/shows/{show_id}
```

Returns details for a specific show by ID.

### Hosts

#### List all hosts
```http
GET /api/v1.0/hosts
```

Returns a list of all hosts.

#### Get a specific host
```http
GET /api/v1.0/hosts/{host_id}
```

Returns details for a specific host by ID.

## Response Schemas

### Broadcast
```json
{
  "id": "integer",
  "start_timestamp": "datetime",
  "end_timestamp": "datetime",
  "episode": {
    // See Episode schema
  },
  "channel": {
    // See Channel schema
  }
}
```

### Episode
```json
{
  "id": "integer",
  "broadcast_title": "string",
  "episode_alias": "string",
  "status": "string",
  "start_timestamp": "datetime",
  "end_timestamp": "datetime",
  "broadcast": "integer",
  "mixcloud_url": "string",
  "show": {
    // See Show schema
  }
}
```

### Show
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "show_alias": "string",
  "external_links": "object",
  "location_short": "string",
  "location_long": "string",
  "intensity": "integer",
  "hosts": [
    // Array of Host objects
  ]
}
```

### Host
```json
{
  "id": "integer",
  "name": "string",
  "bio": "string",
  "image_url": "string",
  "social_links": "object"
}
```

### Channel
```json
{
  "id": "integer",
  "name": "string"
}
```

## Example Usage

Here's an example of how to fetch all current broadcasts using curl:

```bash
curl http://localhost:8000/api/v1.0/broadcasts
```

To get a specific show:

```bash
curl http://localhost:8000/api/v1.0/shows/1
```

The API uses standard HTTP response codes:
- 200: Success
- 404: Not found
- 500: Server error
