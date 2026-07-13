from django.urls import path

from feeds import views

app_name = 'feeds'

urlpatterns = [
    path('', views.home, name='home'),
]
