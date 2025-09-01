

from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import RequestLog, SuspiciousIP




SENSITIVE_PATHS = ['/admin', '/login', '/register']  # add more as needed
REQUEST_THRESHOLD = 100  # requests per hour


@shared_task
def detect_suspicious_ips():
    """
    Anomaly detection task: flags IPs exceeding thresholds or accessing sensitive paths.
    Runs hourly.
    """
    one_hour_ago = now() - timedelta(hours=1)

    # Detect IPs exceeding request threshold
    logs_last_hour = RequestLog.objects.filter(timestamp__gte=one_hour_ago)
    ip_counts = {}
    for log in logs_last_hour:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

    for ip, count in ip_counts.items():
        if count > REQUEST_THRESHOLD:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason=f"Exceeded {REQUEST_THRESHOLD} requests/hour"
            )

    # Detect access to sensitive paths
    sensitive_logs = logs_last_hour.filter(path__in=SENSITIVE_PATHS)
    for log in sensitive_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason=f"Accessed sensitive path: {log.path}"
        )
