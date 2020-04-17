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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import (answer_me, cousin_or_restaurent, tests, search_and_redirect, accept_payment, check_new_orders, accept_or_decline, food_prepared )
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),


     # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
        name='password_change_done'),#template_name='registration/password_change_done.html'

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
        name='password_change'),#template_name='registration/password_change.html'

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),#template_name='registration/password_reset_done.html'

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),#template_name='registration/password_reset_complete.html'

    path('accounts/', include('allauth.urls')),

    path('users/', include('users.urls')),
    path('delivery/', include('Delivery.urls')),
    url('checking/all-order/', check_new_orders, name='check_new_order_json'),
    url('food-prepared/', food_prepared, name='food_prepared'),
    url('accept/decline/', accept_or_decline, name='accept_or_decline'),
    url('ajax/get_response/', answer_me),
    url('ajax/cousin-rest/', cousin_or_restaurent),
    url('ajax/testing/all/', tests, name='testing'),
    url('restaurents/', search_and_redirect, name='restaurents'),
    url('replace-to-paytm/(?P<id>\d+)', accept_payment, name='replace_paytm'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)