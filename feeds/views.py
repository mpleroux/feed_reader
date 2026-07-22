from django.shortcuts import get_object_or_404, render

from .models import Article, Feed


def all_items(request):
    articles = Article.objects.select_related('feed')
    return render(request, 'all_items.html', {'articles': articles})


def feed_detail(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    # noinspection PyUnresolvedReferences
    articles = feed.articles.all()
    return render(request, 'feed_detail.html', {'feed': feed, 'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article.objects.select_related('feed'), pk=article_id)
    return render(request, 'article_detail.html', {'article': article})
