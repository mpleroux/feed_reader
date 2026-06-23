from django.contrib import admin

from .models import Article, Feed, Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'folder', 'last_fetched']
    list_filter = ['folder']
    search_fields = ['title', 'feed_url', 'site_url']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'published', 'is_read']
    list_filter = ['is_read', 'feed', 'published']
    search_fields = ['title', 'author']
    date_hierarchy = 'published'
    list_select_related = ['feed']