from home.views import index , Person
from django.urls import path


urlpatterns = [
    path('index/', index),
    path('person/', Person),
]
