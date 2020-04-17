from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from users.models import *
from django.contrib.auth.decorators import login_required
from website.settings import EMAIL_HOST_USER
from django.urls import reverse
import datetime

def in_duty(request):
    id = request.user.id
    Shippers.objects.filter(shipper=id).update(start_duty=True)
    return HttpResponseRedirect(reverse('delivery_home'))

def out_duty(request):
    id=request.user.id
    Shippers.objects.filter(shipper=id).update(start_duty=False)
    return HttpResponseRedirect(reverse('delivery_home'))


@login_required(login_url = '/users/delivery/login/')
def get_order(request):
    ids = request.session['d_id']
    all_order = Orders.objects.filter(
        Q(order_statuses='RD', shipper_id=ids) | Q(order_statuses='P&D', shipper_id=ids) | Q(order_statuses='A&P', shipper_id=ids)
    )
    if all_order:
        
        user_id = userAddress.objects.filter(user=all_order[0].user_id)
        restaurent = Restaurents.objects.filter(orders__id=all_order[0].id)
        total_order =Orderdetails.objects.filter(order_id= all_order[0].id).count()
        data={
            'all_order': serializers.serialize('json', all_order),
            'id': serializers.serialize('json', user_id),
            'restaurent': serializers.serialize('json', restaurent),
            'items_no': total_order,

        }

        return JsonResponse(data, safe=False)

    else:
        return HttpResponse('nothing')


@login_required(login_url = '/users/delivery/login/')
def update_request(request):
    id = request.GET.get('id')[6:]
    Orders.objects.filter(id=id).update(order_statuses='P&D')
    data={
        'data': id
    }
    return JsonResponse(data, safe=False)

def order_rejected(request):
    shipper_id = Shippers.objects.get(shipper = request.user.id).id
    shiper = Shippers.objects.filter(start_duty=True).exclude(id=shipper_id)[:1]
    print(shiper[0].id)
    
def delivered(request):
    id = request.GET.get('id')[4:]
    Orders.objects.filter(pk=id).update(order_statuses='S')
    orders = Orders.objects.get(pk=id)
    user = orders.user_id.email
    rest = orders.restaurents_id.user.email
    subject = 'Your Last Minute Labor  order no.' + id + "has been delivered."
    message = "Hi,"\
              " Thanks for using Last Minute Labor! Your order from "+ str(orders.restaurents_id.name) + " has been delivered." \
              "looking forword to serving you again."
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [user, rest],
        fail_silently=False,
    )
    data={
        'status': 'ok'
    }
    return JsonResponse(data, safe=False)