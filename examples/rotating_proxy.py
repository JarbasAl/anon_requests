from anon_requests import RotatingProxySession
from anon_requests import ProxyType

# validate=True will check if all proxies are functioning (default False)
# validated proxies will be used first
# bad proxies will be tried once you run out of good proxies
# everytime it runs out of unused proxies, it will start reusing old ones
# pass ignore_bad=False to not try the bad proxies at all (default True)
with RotatingProxySession(proxy_type=ProxyType.SOCKS5, validate=True) \
        as session:
    for i in range(50):
        # every request rotates proxy before being made
        # keeps trying until we get 200 status code
        # will only repeat a proxy once all have been tried
        # this means it can hang for a while here until request succeeds
        response = session.get('https://ipecho.net/plain', timeout=5)
        print(response.text)  # Not your ip address, different every time

        # NOTE: infinite proxy rotating loop is not impossible but unlikely
        # TODO max retries parameter (per request)
