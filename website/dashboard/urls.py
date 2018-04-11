from django.conf.urls import include, url
from dashboard import views as dash_views
urlpatterns = [
    url(r'^$',dash_views.home,name='dashhome')
]
