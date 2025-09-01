

import logging
from django.utils.timezone import now
from ip_tracking.models import RequestLog
from ip_tracking.models import BlockedIP
from django.http import HttpResponseForbidden
from django.core.cache import cache
from IpGeoLocation import IpGeoLocation


logger = logging.getLogger(__name__)

class IPLoggingMiddleware:
    """
    Middleware to log the IP address of each incoming request.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.geo = IpGeoLocation(api_key=None)  # If API key is required, pass here

    def __call__(self, request):
        # Get the client's IP address
        ip_address = self.get_client_ip(request)
        
        # Check blacklist
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            logger.warning(f"Blocked request from blacklisted IP: {ip_address}")
            return HttpResponseForbidden("Your IP has been blocked.")
        
        # Geolocation lookup with caching
        cache_key = f"geo:{ip_address}"
        geo_data = cache.get(cache_key)

        if not geo_data:
            try:
                geo_info = self.geo.get_geolocation(ip_address)
                geo_data = {
                    "country": geo_info.get("country_name", ""),
                    "city": geo_info.get("city", "")
                }
                cache.set(cache_key, geo_data, timeout=60 * 60 * 24)  # 24 hours
            except Exception as e:
                logger.error(f"Failed to fetch geolocation for {ip_address}: {e}")
                geo_data = {"country": "", "city": ""}

        
        # Log the request details to the database
        # save log entry
        try:
            RequestLog.objects.create(
                ip_address=ip_address,
                timestamp=now(),
                path=request.path,
                country=geo_data.get("country", ""),
                city=geo_data.get("city", "")
            )
        except Exception as e:
            logger.error(f"Failed to log request: {e}")

        # Proceed with the request processing
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Retrieve the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip