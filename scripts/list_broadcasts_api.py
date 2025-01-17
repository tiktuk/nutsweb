#!/usr/bin/env python3
import requests
import sys
from datetime import datetime
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description="List broadcasts from NTS API")
    parser.add_argument(
        "--channel",
        type=int,
        choices=[1, 2],
        help="Filter broadcasts by channel number (1 or 2)",
    )
    args = parser.parse_args()

    try:
        response = requests.get("http://localhost:8000/api/broadcasts")
        response.raise_for_status()
        broadcasts = response.json()

        # Filter by channel if specified
        if args.channel:
            broadcasts = [b for b in broadcasts if b["channel"]["name"] == str(args.channel)]

        # Sort by start timestamp
        broadcasts.sort(key=lambda x: x["start_timestamp"])

        current_date = None

        for broadcast in broadcasts:
            start_time = datetime.fromisoformat(broadcast["start_timestamp"].replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(broadcast["end_timestamp"].replace("Z", "+00:00"))
            broadcast_date = start_time.date()

            # Add day marker if we're on a new day
            if current_date != broadcast_date:
                current_date = broadcast_date
                print(f"\n=== {current_date.strftime('%A, %B %d, %Y')} ===\n")

            # Format and display broadcast info
            print(
                f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')} | "
                f"{broadcast['channel']['name']} | "
                f"{broadcast['episode']['broadcast_title']}"
            )

    except requests.exceptions.RequestException as e:
        print(f"Error fetching broadcasts: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
