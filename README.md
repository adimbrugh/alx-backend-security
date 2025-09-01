📌 IP Tracking: Security & Analytics (Django)

This module provides IP tracking, blacklisting, geolocation, rate limiting, and anomaly detection for Django applications.
It is part of the alx-backend-security repository.

---

🚀 Features

Request Logging → Logs IP address, timestamp, request path (+ geolocation).

IP Blacklisting → Blocks requests from harmful IPs (403 Forbidden).

Geolocation Analytics → Enriches logs with country & city (cached for 24h).

Rate Limiting → Prevents abuse (per-IP throttling).

Anomaly Detection → Flags suspicious IPs (excessive requests, sensitive paths).

---

📂 Directory Structure
ip_tracking/
├── __init__.py
├── admin.py
├── apps.py
├── middleware.py
├── models.py
├── tasks.py
├── views.py
└── management/
    └── commands/
        ├── block_ip.py
        └── unblock_ip.py


---

⚙️ Installation

Install dependencies:

pip install django-ipware django-ipgeolocation django-ratelimit celery redis


Add ip_tracking to INSTALLED_APPS in settings.py:

INSTALLED_APPS = [
    ...
    'ip_tracking',
]


Register middleware in settings.py:

MIDDLEWARE = [
    ...
    "ip_tracking.middleware.IPLoggingMiddleware",
]


Configure Celery (in celery.py):

from celery.schedules import crontab

app.conf.beat_schedule = {
    'detect-suspicious-ips-hourly': {
        'task': 'ip_tracking.tasks.detect_suspicious_ips',
        'schedule': crontab(minute=0, hour='*'),
    },
}

---

📊 Models

RequestLog → Stores IP, timestamp, path, country, city.

BlockedIP → Stores IPs to block (403 Forbidden).

SuspiciousIP → Stores flagged IPs with reasons.

Run migrations:

python manage.py makemigrations ip_tracking
python manage.py migrate

---

🛡️ Usage
1. Logging Requests

Every incoming request is logged in RequestLog with geolocation data.

2. Blocking & Unblocking IPs

Block an IP:

python manage.py block_ip 192.168.1.10


Unblock an IP:

python manage.py unblock_ip 192.168.1.10

3. Rate Limiting

Applied to sensitive views (example: /login):

Anonymous users: 5 requests/min

Authenticated users: 10 requests/min

If exceeded → returns 429 Too Many Requests.

4. Anomaly Detection

Runs hourly via Celery:

Flags IPs making 100+ requests/hour

Flags IPs accessing sensitive paths (/admin, /login)

Results stored in SuspiciousIP.

---

📌 Example Suspicious Activity Flow

A bot hits /login 200 times in 1 hour.

Celery task flags IP → entry in SuspiciousIP.

(Future) Admin can auto-block flagged IPs.

⚖️ Ethical & Legal Considerations

Privacy: Truncate or anonymize IPs where required.

Compliance: Follow GDPR/CCPA data retention & transparency rules.

Fairness: Avoid blanket blocking entire regions.

---

✅ Roadmap

 Request Logging

 Blacklisting

 Geolocation Analytics

 Rate Limiting

 Anomaly Detection

 Automatic Blocking of Suspicious IPs

 Admin Dashboard with Geo Charts

📌 With this module, Django apps can track, analyze, and protect against malicious IP activity while maintaining compliance and ethics.