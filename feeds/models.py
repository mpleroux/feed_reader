from urllib.parse import urlparse

from django.db import models
from django.utils import timezone


class Folder(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Feed(models.Model):
    folder = models.ForeignKey(
        Folder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feeds',
    )
    title = models.CharField(max_length=255)
    site_url = models.URLField(max_length=500, blank=True)
    feed_url = models.URLField(max_length=500, unique=True)
    # Conditional-GET cache headers from the last fetch
    etag = models.CharField(max_length=255, blank=True)
    last_modified = models.CharField(max_length=255, blank=True)
    last_fetched = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def favicon_url(self):
        domain = urlparse(self.site_url).netloc or urlparse(self.feed_url).netloc
        return f'https://icons.duckduckgo.com/ip3/{domain}.ico'


class Article(models.Model):
    feed = models.ForeignKey(
        Feed,
        on_delete=models.CASCADE,
        related_name='articles',
    )
    guid = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=255, blank=True)
    link = models.URLField(max_length=500)
    published = models.DateTimeField(null=True, blank=True)
    content = models.TextField(blank=True)
    excerpt = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published']
        constraints = [
            models.UniqueConstraint(
                fields=['feed', 'guid'],
                name='unique_guid_per_feed',
            ),
        ]

    def __str__(self):
        return self.title

    @property
    def published_day(self):
        # Local-timezone midnight of the published date, so articles from the
        # same local day share one grouper value (and naturalday sees the tzinfo)
        if self.published is None:
            return None
        return timezone.localtime(self.published).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
