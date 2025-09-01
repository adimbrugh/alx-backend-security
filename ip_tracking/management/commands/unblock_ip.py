

from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP



class Command(BaseCommand):
    help = "Unblock an IP address by removing it from the BlockedIP model."

    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str, help="The IP address to unblock")

    def handle(self, *args, **options):
        ip_address = options["ip_address"]

        try:
            blocked_ip = BlockedIP.objects.filter(ip_address=ip_address).first()
            if not blocked_ip:
                self.stdout.write(self.style.WARNING(f"IP {ip_address} is not in the blacklist."))
                return

            blocked_ip.delete()
            self.stdout.write(self.style.SUCCESS(f"Successfully unblocked IP: {ip_address}"))

        except Exception as e:
            raise CommandError(f"Error unblocking IP {ip_address}: {e}")
