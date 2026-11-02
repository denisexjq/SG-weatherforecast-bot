# SG Weatherforecast Bot — @sg_weatherforecast_bot

Telegram bot: **[@sg_weatherforecast_bot](https://t.me/sg_weatherforecast_bot)**

Sends Singapore rain-probability updates, once a day automatically, plus
on-demand rechecks. No token is stored in this repo — set `BOT_TOKEN` in the
environment (see "Environment variables" below).

## Bot handle

- Handle: `@sg_weatherforecast_bot`
- Open it in Telegram: https://t.me/sg_weatherforecast_bot
- Start it with `/start` — that is how the daily 8am update learns which
  chats to send to. There is no admin requirement to post.
- Try it with `/recheck` (Jurong West), or `/recheck queenstown`,
  `/recheck bedok`, `/recheck tampines` for another Singapore region.

## What it does

- **Daily, 8am Asia/Singapore, Jurong West only:** one message to every chat
  that has sent `/start` to the bot (private chats and groups — the chat ID
  differs per chat, there is no single fixed channel ID). No other automatic
  messages.
- **On demand:** `/recheck` in Telegram replies once, only to that chat.
  `/recheck <region>` checks that region **in Singapore only**
  (for example `/recheck queenstown` means Queenstown, Singapore, never
  Queenstown in another country). A region command is never skipped just
  because no distinct postcode page exists for it — use the best
  "<region>, Singapore" hourly result and that result's URL as the link.

## Forecast source

- Primary source: **Weather.com** hourly Rain %, mm, and condition.
- Jurong West default, postcode **644664** (not 638366):
  https://weather.com/en-CA/sg/south-west-community-development-council/postcode/644664/hourbyhour
- The daily 8am update stays Jurong West only, even when a recheck used
  another region.

## Message format (exact)

Title line, date line, a blank line between periods, a line break after each
period's colon, each hour on its own line. Only hours with rain chance
**40% or more** are included; a period with no such hours is omitted
entirely. Each included hour has only time, percentage, and one intensity
phrase: `small showers` for light showers / low mm, `big showers` for heavy
showers / higher mm, and `Thunderstorm` in place of `big showers` where the
forecast condition is a thunderstorm. No other wording.

After the last period, a blank line, then the manual-check link on its own
separate line, inside the same single message — never as a separate message.

```
Jurong West Rain probability
Today, 2 November 2026

Afternoon 12pm–5pm:
3pm 62% small showers
4pm 44% small showers

Evening 5pm–10pm:
5pm 42% small showers

https://weather.com/en-CA/sg/south-west-community-development-council/postcode/644664/hourbyhour
```

Periods: Morning 7am–12pm, Afternoon 12pm–5pm, Evening 5pm–10pm.

For a region recheck, the title and link change to that Singapore region,
for example `Queenstown Rain probability`.

## Deduplication

Track processed Telegram `update_id`s in `seen_updates.json`
(ignored by git, see `.gitignore`):

```json
{"seen_update_ids": [983213231, 983213232]}
```

A `/recheck` is answered once, and only after answering is its
`update_id` added. `/start` is never answered by the recheck watcher.

## Environment variables

Only one is required by the code in this repo:

| Variable | Required | What it is / how to set it |
| --- | --- | --- |
| `BOT_TOKEN` | Yes | The Telegram bot token for `@sg_weatherforecast_bot`. Get it from [@BotFather](https://t.me/BotFather) (`/mybots` → your bot → API Token). Set it in the environment only — never put it in a file you commit. |

No other variables are needed: chat IDs are discovered from `getUpdates`
after a chat sends `/start`, and the default region (Jurong West, 644664)
is in the spec above, not in an env var.

Changes to make when you set this up somewhere new:

1. **Get / reuse the token:** do not create a new bot unless you want a new
   handle — this README is for `@sg_weatherforecast_bot`, so reuse its
   existing token from BotFather.
2. **Local run:**
   ```sh
   export BOT_TOKEN='<your bot token>'
   python3 telegram.py getMe
   ```
   `getMe` should return `username: sg_weatherforecast_bot`. If it
   returns 401, the token is wrong; if 404, the token is malformed.
3. **Do not use a `.env` file in git:** `.env` and `seen_updates.json`
   are in `.gitignore`. For a server, put the token in a service
   environment file or secret store instead, for example a systemd
   `EnvironmentFile=` or your host's secret manager — not in the repo.
4. **GitHub Actions (if you add a workflow later):** add `BOT_TOKEN` as a
   repository secret (Settings → Secrets and variables → Actions), and
   reference it as `${{ secrets.BOT_TOKEN }}` in the workflow. Do not
   paste it into a workflow file.
5. **Schedule / timezone:** the daily job is 8am **Asia/Singapore**.
   Whatever scheduler you use (cron, GitHub Actions, systemd timer), set
   its timezone to `Asia/Singapore` — a UTC 8am job would run at 4pm
   Singapore time.
6. **Rotate if leaked:** if a token ever appears in git, a screenshot, or
   a log, revoke it in BotFather (`/revoke`) and update the secret
   everywhere it is set. The old token stops working immediately.

## Running it

```sh
export BOT_TOKEN='<your bot token>'
python3 telegram.py getMe
python3 telegram.py getUpdates
python3 telegram.py sendMessage --chat-id <chat-id> --text '<message>'
```

Python 3, standard library only. No dependencies to install.
