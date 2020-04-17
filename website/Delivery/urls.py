from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('start-duty/', views.in_duty, name='duty'),
    path('out-duty/', views.out_duty, name='out_duty'),
    path('get/new-delivery/', views.get_order, name='checking_order'),
    path('order/pick-up/', views.update_request, name='order_pickup'),
    path('order/rejects/', views.order_rejected, name='order_reject'),
    path('order/delivered/', views.delivered, name='order_success'),


]