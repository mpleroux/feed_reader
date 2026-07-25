from django.core.management.base import BaseCommand

from feeds.models import Feed, Folder
from feeds.services import fetch_feed

# Demo feeds for the deployed read-only demo. Grouped into a folder to show off
# sidebar grouping; Hacker News is left unfiled on purpose to show that case too.
DEMO_FEEDS = [
    {
        'title': 'Django Blog',
        'feed_url': 'https://www.djangoproject.com/rss/weblog/',
        'site_url': 'https://www.djangoproject.com/',
        'folder': 'Development',
    },
    {
        'title': 'Simon Willison',
        'feed_url': 'https://simonwillison.net/atom/everything/',
        'site_url': 'https://simonwillison.net/',
        'folder': 'Development',
    },
    {
        'title': 'Hacker News',
        'feed_url': 'https://hnrss.org/frontpage',
        'site_url': 'https://news.ycombinator.com/',
        'folder': None,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with demo feeds and fetch their articles (idempotent)'

    def handle(self, *args, **options) -> str | None:
        for entry in DEMO_FEEDS:
            folder = None
            if entry['folder']:
                folder, _ = Folder.objects.get_or_create(name=entry['folder'])

            feed, created = Feed.objects.get_or_create(
                feed_url=entry['feed_url'],
                defaults={
                    'title': entry['title'],
                    'site_url': entry['site_url'],
                    'folder': folder,
                },
            )
            verb = 'Created' if created else 'Exists '
            self.stdout.write(f'{verb} {feed.title}')

            new_count = fetch_feed(feed)
            self.stdout.write(self.style.SUCCESS(f'  fetched {new_count} new articles'))

        self.stdout.write(self.style.SUCCESS('Seed complete'))
