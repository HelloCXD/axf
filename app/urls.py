from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^market/(\d+)/(\d+)/(\d+)$', views.market, name='market'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^mine/$', views.mine, name='mine'),
    url(r'^registe/$', views.registe , name='registe'),
    url(r'^checkaccount/$', views.checkaccount, name='checkaccount'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]