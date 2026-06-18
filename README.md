# README

A single-user RSS/Atom feed reader built with Python and Django. Work-in-progress.

## Features

Planned capabilities:

- **Feed management** — Add feeds by URL, autodiscover feeds from a site URL, organize feeds into folders, rename and delete
- **Reading** — Unified "All Items" view, per-feed views, and a clean article reader with sanitized HTML and images
- **Organization** — Articles grouped by date ("Today", "Yesterday"), with favicons and per-feed grouping in the sidebar
- **Read/unread tracking** — Toggle read state, mark all as read, and unread counts per feed
- **Search** — Filter the current view by keyword
- **Live interaction** — Read/unread toggles and on-demand refresh without full page reloads, via `htmx`
- **Background refresh** — Scheduled fetching of new articles

## Tech Stack

I will be implementing a deliberately Python-centric stack — no separate JS framework, no Node.js build step.

| Layer           | Technology                                                            |
|-----------------|-----------------------------------------------------------------------|
| Language        | Python 3.13                                                           |
| Framework       | Django 6.0                                                            |
| Feed parsing    | `feedparser` (RSS + Atom)                                             |
| Feed discovery  | `requests` + `BeautifulSoup`                                          |
| HTML sanitizing | `nh3`                                                                 |
| Interactivity   | `htmx` + `django-htmx`                                                |
| Styling         | Tailwind CSS v4 (via `django-tailwind-cli`, standalone — no Node.js)  |
| Database        | SQLite                                                                |
| Tooling         | `uv` (env + packages), `Ruff` (lint/format), `django-debug-toolbar`   |
| Testing         | Django TestCase                                                       |

## Run Locally

## Architecture

## Design inspiration

The simple UI for this project is loosely based on the iOS app [Reeder Classic](https://reederapp.com/classic/), the older and more traditional RSS reader app offered by that author. Other RSS readers I have used like Google Reader (RIP) were also influential.

## Future enhancements

Stretch goals: full-text search, cached favicons, OPML import/export, and multi-user accounts.
