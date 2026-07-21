from django.urls import path

from feeds import views

app_name = 'feeds'

urlpatterns = [
    path('', views.all_items, name='all_items'),
    path('feed/<int:feed_id>/', views.feed_detail, name='feed_detail'),
]
