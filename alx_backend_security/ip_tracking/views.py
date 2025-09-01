from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit
from django.http import JsonResponse




# Anonymous users: 5 req/min
anon_rate = '5/m'

# Authenticated users: 10 req/min
auth_rate = '10/m'


@csrf_exempt
@ratelimit(key='ip', rate=anon_rate, method='POST', block=True)
@ratelimit(key='ip', rate=auth_rate, method='POST', block=False)
def login_view(request):
    """
    A dummy login view demonstrating IP-based rate limiting.
    """

    # Determine if the request exceeded the limit
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({'error': 'Too many requests'}, status=429)

    # Example login logic (dummy)
    return JsonResponse({'message': 'Login successful'})
