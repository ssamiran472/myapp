from django.http import JsonResponse
from users.models import *

def update_request(request):
    id = request.GET.get('id')[7:]
    Orders.objects.filter(id=id).update(order_statuses='P&D')
    data={
        'data': id
    }
    return JsonResponse(data, safe=False)