#!/usr/bin/env python3
"""Standalone Telegram helper for @sg_weatherforecast_bot.

Reads the bot token from the BOT_TOKEN environment variable only.
Never commit a token, a .env file, or seen_updates.json to git.

Usage:
  BOT_TOKEN=... python3 telegram.py getMe
  BOT_TOKEN=... python3 telegram.py getUpdates
  BOT_TOKEN=... python3 telegram.py sendMessage --chat-id 56011594 --text 'Hello'
"""
import argparse
import json
import os
import sys
import urllib.request


def call(method, payload=None):
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise SystemExit("BOT_TOKEN is not set")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        url, data=data, headers=headers, method="POST" if payload is not None else "GET"
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("getMe")
    sub.add_parser("getUpdates")
    send = sub.add_parser("sendMessage")
    send.add_argument("--chat-id", required=True)
    send.add_argument("--text", required=True)
    args = parser.parse_args()
    if args.command == "getMe":
        result = call("getMe")
    elif args.command == "getUpdates":
        result = call("getUpdates")
    else:
        result = call("sendMessage", {"chat_id": args.chat_id, "text": args.text})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
