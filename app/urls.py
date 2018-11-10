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

    url(r'^addcart/$', views.addcart, name='addcart'),
    url(r'^subcart/$', views.subcart, name='subcart'),

    url(r'^changecartstatus/$', views.changecartstatus, name='changecartstatus'), # 修改选中状态
    url(r'changecartselect/$', views.changecartselect,name='changecartselect'), # 全选/取消全选

    url(r'^generateorder/$', views.generateorder, name='generateorder'),  # 下单
    url(r'^orderinfo/(\d+)/$', views.orderinfo, name='orderinfo'), # 订单信息


]