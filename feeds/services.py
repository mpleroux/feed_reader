import calendar
from datetime import UTC

import feedparser
from django.utils import timezone

from .models import Article, Feed


# noinspection PyUnresolvedReferences
def _parse_published(entry) -> timezone.datetime | None:
    if not entry.get('published_parsed'):
        return None
    timestamp = calendar.timegm(entry.published_parsed)
    return timezone.datetime.fromtimestamp(timestamp, tz=UTC)


def fetch_feed(feed: Feed) -> int:
    # noinspection PyTypeChecker
    parsed = feedparser.parse(
        feed.feed_url,
        etag=feed.etag or None,
        modified=feed.last_modified or None,
    )

    if parsed.get('status') == 304:
        feed.last_fetched = timezone.now()
        feed.save(update_fields=['last_fetched'])
        return 0

    new_articles = 0
    for entry in parsed.entries:
        _, created = Article.objects.get_or_create(
            feed=feed,
            guid=entry.get('id', entry.link),
            defaults={
                'title': entry.title,
                'author': entry.get('author', ''),
                'link': entry.link,
                'published': _parse_published(entry),
                'content': entry.get('summary', ''),
                'excerpt': entry.get('summary', '')[:300],
            },
        )
        if created:
            new_articles += 1

    feed.etag = parsed.get('etag', '')
    feed.last_modified = parsed.get('modified', '')
    feed.last_fetched = timezone.now()
    feed.save(update_fields=['etag', 'last_modified', 'last_fetched'])

    return new_articles