from django.core.management.base import BaseCommand
import datetime
from users.models import Orders
class Command(BaseCommand):
    help='Displays current time'

    def handle(self, *args, **options):
        time = datetime.datetime.now().timestamp()
        all_orders = Orders.objects.filter(stautus=False)
        for order in all_orders:
            time_in_sec = order.order_date_and_time.timestamp()
            time_diff= int(time) - int(time_in_sec)
            time_diff_in_minute = time_diff/60
            if time_diff_in_minute > 1:
                order.delete()

        self.stdout.write("delete done..  %s")
