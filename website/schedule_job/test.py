from users.models import Orders
import datetime

def Coding():
    time = datetime.datetime.now().timestamp()
    all_order = Orders.objects.filter(order_statuses='O')
    for order in all_order:
        time_in_sec = order.order_date_and_time.timestamp()
        time_diff = int(time) - int(time_in_sec)
        time_diff_in_minute = time_diff / 60
        if time_diff_in_minute > 50:
            Orders.objects.filter(id=order.id).update(order_statuses="R")

    print('done')