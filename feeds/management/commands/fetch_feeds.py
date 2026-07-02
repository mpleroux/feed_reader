from django.core.management.base import BaseCommand

from feeds.models import Feed
from feeds.services import fetch_feed


class Command(BaseCommand):
    help = 'Fetch feeds'

    def handle(self, *args, **options) -> str | None:
        total_articles: int = 0
        for feed in Feed.objects.all():
            new_count: int = fetch_feed(feed)
            if new_count > 0:
                self.stdout.write(self.style.SUCCESS(f'{feed.title}: {new_count} new'))
            else:
                self.stdout.write(self.style.NOTICE(f'{feed.title}: No new'))
            total_articles += new_count
        self.stdout.write(self.style.NOTICE(f'Total new articles: {total_articles}'))
