from anon_requests.proxy import ProxyLeech
from anon_requests import RotatingProxySession
from anon_requests import ProxyType

leech = ProxyLeech(workers=100, verbose=False, timeout=2)
proxies = leech.get_proxy_list()
print("Validating proxies (this might take a while)", "TOTAL", len(proxies))
leech.validate()
print("GOOD", len(leech.good_proxies), "BAD", len(leech.bad_proxies),
      "GOOD/BAD", len(leech.good_proxies)/len(leech.bad_proxies))


leech.remove_bad_proxies()  # remove bad proxies from pool
assert len(leech.good_proxies) == len(leech.all_proxies)

# pass leech to ProxySession, validated proxies will be used first
# bad proxies will be tried once you run out of good proxies
# everytime it runs out of unused proxies, all good proxies will once more be
# used before bad proxies
with RotatingProxySession(proxy_provider=leech, proxy_type=ProxyType.SOCKS5) \
        as session:
    for i in range(50):
        # every request rotates proxy before being made
        # keeps trying until we get 200 status code
        # will only repeat a proxy once all have been tried
        # this means it can hang for a while here until request succeeds
        response = session.get('https://ipecho.net/plain', timeout=5)
        print(response.text)  # Not your ip address

        # NOTE: infinite proxy rotating loop is not impossible but unlikely
        # TODO max retries parameter (per request)
