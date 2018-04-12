from django.conf.urls import include, url
from dashboard import views as dash_views

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', dash_views.index, name='index'),
    url(r'patient/', dash_views.home, name='dashhome'),

]
