from django.shortcuts import render

from .models import Article


def all_items(request):
    articles = Article.objects.select_related('feed')
    return render(request, 'all_items.html', {'articles': articles})
