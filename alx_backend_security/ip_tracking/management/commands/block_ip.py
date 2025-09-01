

from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP



# Command to block an IP address
class Command(BaseCommand):
    help = 'Block an IP address'
    
    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            self.stdout.write(self.style.WARNING(f'IP address {ip_address} is already blocked.'))
            return
        
        try:
            BlockedIP.objects.create(ip_address=ip_address)
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP address: {ip_address}'))
        except Exception as e:
            raise CommandError(f'Error blocking IP address {ip_address}: {e}')
