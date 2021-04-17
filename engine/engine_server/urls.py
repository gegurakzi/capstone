from django.urls import path
from . import views
 
app_name = 'engine_server'
urlpatterns = [
    path('',  views.Video.as_view(), name='video'),
]
