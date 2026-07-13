from datetime import UTC, datetime
from unittest.mock import patch

import feedparser
from django.test import TestCase

from .models import Article, Feed
from .services import fetch_feed

SAMPLE_PUBLISHED = datetime(2026, 7, 9, 17, 0, tzinfo=UTC)


def make_entry(**overrides):
    defaults = {
        'id': 'guid-1',
        'title': 'Test Article',
        'link': 'https://example.com/test-article',
        'author': 'Jane Doe',
        'published_parsed': SAMPLE_PUBLISHED.timetuple(),
        'summary': '<p>Hello world</p>',
    }
    defaults.update(overrides)
    return feedparser.FeedParserDict(defaults)


class FetchFeedTests(TestCase):
    def setUp(self):
        self.feed = Feed.objects.create(
            title='Test Feed', feed_url='https://example.com/feed.xml'
        )

    @patch('feeds.services.feedparser.parse')
    def test_dedupes_by_guid(self, mock_parse):
        mock_parse.return_value = feedparser.FeedParserDict(
            {'status': 200, 'entries': [make_entry()]}
        )

        first_count = fetch_feed(self.feed)
        second_count = fetch_feed(self.feed)

        self.assertEqual(first_count, 1)
        self.assertEqual(second_count, 0)
        self.assertEqual(Article.objects.count(), 1)

    @patch('feeds.services.feedparser.parse')
    def test_normalizes_published_date_to_utc(self, mock_parse):
        mock_parse.return_value = feedparser.FeedParserDict(
            {'status': 200, 'entries': [make_entry()]}
        )

        first_count = fetch_feed(self.feed)
        article = Article.objects.get()

        self.assertEqual(first_count, 1)
        self.assertEqual(article.published, SAMPLE_PUBLISHED)

    @patch('feeds.services.feedparser.parse')
    def test_missing_published_date_is_none(self, mock_parse):
        mock_parse.return_value = feedparser.FeedParserDict(
            {'status': 200, 'entries': [make_entry(published_parsed=None)]}
        )

        first_count = fetch_feed(self.feed)
        article = Article.objects.get()

        self.assertEqual(first_count, 1)
        self.assertIsNone(article.published)
