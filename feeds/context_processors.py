from .models import Feed, Folder


def sidebar_feeds(request):
    return {
        'sidebar_folders': Folder.objects.prefetch_related('feeds'),
        'sidebar_unfiled_feeds': Feed.objects.filter(folder__isnull=True),
    }