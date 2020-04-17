"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # users urls
    path('', views.index, name='overview'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('home/all-restaurents/', views.home_all_restaurents, name='all'),
    path('home/your-order/', views.order_now, name='order'),
    path('home/dinner/<id>/orders/', views.order_details, name='orders'),
    path('home/restaurent-full-specification/<id>/', views.specification, name='specification_of_restaurent'),
    path('home/restaurents-in/<locality>/', views.locality, name='locality'),
    path('home/restaurent-full-specification/(?P<id>\d+)/(?p<rate>\d+)/', views.ratings, name='rate'),
    path('home/restaurent-full-specification/(?P<id>\d+)/add-review/', views.reviews, name='reviews'),
    path('home/restaurents/<name>/', views.cuisine, name='cuisines'),
    path('home/order-history/', views.order_history, name='orderhistory'),
    path('rearch-result/', views.searching, name='search'),
    path('payment/', views.payment, name='payment'),
    path('handlerequest/', views.handelrequest, name='handelrequest'),
    path('all-restaurents-ratings-heigh-to-low/', views.ratings_hight_to_low, name='ratings_hight_to_low'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

# dellivery partner urls
    path('delivery/', views.delivery_partner, name='delivery_partner'),
    path('delivery/login/', views.delivery_login, name='delivery_login'),
    path('delivery/home/', views.delivery_home, name='delivery_home'),

# restaurent users urls
    path('restaurent/', views.restaurents, name='restaurent'),
    path('restaurent/login/', views.restaurents_login, name='restaurent_login'),
    path('restaurent/home/', views.restaurents_home, name='restaurent_home'),
    path('restaurent/home/cat/', views.addCategory, name='category'),
    path('restaurent/home/cat/f/', views.addfood, name='addfood'),
    path('restaurent/home/cat/delete/<id>/', views.delete_category, name='delete_category'),
    path('restaurent/all-reviews/', views.show_reviews, name='restaurent_review'),
    path('restaurent/all_orders/', views.all_orders, name='all_orders'),
    url('restaurent/order/checking/', views.order_info, name='order_info'),
    path('restaurent/get-order/', views.check_order, name='go_order_page'),


]

