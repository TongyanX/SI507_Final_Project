"""WebData URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from WebData import views, dataAJAX

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^table/$', views.table, name='table'),
    url(r'^table/univ/$', views.table_univ, name='table_univ'),
    url(r'^table/gdp/$', views.table_gdp, name='table_gdp'),
    url(r'^plot/$', views.plot, name='plot'),

    url(r'^univ/$', dataAJAX.state_univ, name='state_univ'),
    url(r'^gdp/$', dataAJAX.state_gdp, name='state_gdp'),
    url(r'^plot/bar/$', dataAJAX.bar, name='bar'),
    url(r'^plot/line/$', dataAJAX.line, name='line'),
    url(r'^plot/histogram/$', dataAJAX.histogram, name='histogram'),
    url(r'^plot/bubble/$', dataAJAX.bubble, name='bubble'),
    url(r'^plot/scatter/$', dataAJAX.scatter, name='scatter'),
    url(r'^plot/map/$', dataAJAX.mapbox, name='mapbox'),
]
