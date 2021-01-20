from anon_requests.proxy import ProxyLeech

# ProxyLeech will scrap proxies from all providers, but you can also import a
# specific provider, see anon_requests.proxy_sources
leech = ProxyLeech(workers=100, verbose=False, timeout=2)

proxies = leech.get_proxy_list()  # scrap

print("Validating proxies (this might take a while)", "TOTAL", len(proxies))
leech.validate()  # verify if proxies are functional

print("GOOD", len(leech.good_proxies),
      "BAD", len(leech.bad_proxies),
      "GOOD/BAD", len(leech.good_proxies)/len(leech.bad_proxies))

leech.remove_bad_proxies()  # remove bad proxies from pool
assert len(leech.good_proxies) == len(leech.all_proxies)

# do stuff
proxy = leech.get()  # new proxy on every call to .get
print(proxy)  # dict with proxy info
