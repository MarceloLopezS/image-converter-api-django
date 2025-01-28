from django.core.cache import caches
from django.http import JsonResponse

def rate_limit(key='ip', rate = '20/d'):
    """
    Decorator function.

    Recieves a key string as identification method for the client.
    Recieves a rate string to determine the request count limit in a 
    given time frame.

    The time frame accepts s, 'm', 'h, 'd' to refer seconds, 
    minutes, hours and days respectively.
    """
    cache = caches['ratelimit']
    cache_key_format = 'rl_%(ip)s'

    def get_client_ip(request):
        ip = None
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        return ip

    def get_cache_key(request):
        return cache_key_format % { 'ip': get_client_ip(request) }

    def parse_rate(rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        num, period = rate.split('/')
        num_requests = int(num)
        duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]
        
        return (num_requests, duration)
    
    def inner(func):
        def wrapper(request):
            RATE_LIMIT, TIME_PERIOD = parse_rate(rate)

            if key == 'ip':
                cache_key = get_cache_key(request)
                request_count = cache.get(cache_key)

                if request_count is None:
                    cache.set(cache_key, 0, timeout=TIME_PERIOD)
                    request_count = 0
                
                if request_count >= RATE_LIMIT:
                    return JsonResponse({
                        'status': 'fail',
                        'data': {
                            'message': 'Daily request limit reached.'
                        }
                    }, status=429)
                
                cache.incr(cache_key)
            
            return func(request)
        
        return wrapper
    
    return inner
