# Anon Requests

anonymous python requests

## Install

```bash
pip install anon_requests
```

## Usage

see [examples folder](./examples) for more use cases

Proxies
```python
from anon_requests import RotatingProxySession
from anon_requests import ProxyType

# validate=True will check if all proxies are functioning (default False)
# validated proxies will be used first
# "bad" proxies will be tried once you run out of good proxies
# everytime it runs out of unused proxies, it will start reusing old ones
# pass ignore_bad=False to not try the "bad" proxies at all (default True)
with RotatingProxySession(proxy_type=ProxyType.SOCKS5, validate=True) \
        as session:
    for i in range(50):
        # every request rotates proxy before being made
        # keeps trying until we get 200 status code
        # will only repeat a proxy once all have been tried
        # this means it can hang for a while here until request succeeds
        response = session.get('https://ipecho.net/plain', timeout=5)
        print(response.text)  # Not your ip address, different every time
```

Tor
```python
from anon_requests import RotatingTorSession

# Choose a proxy port, a control port, and a password.
# Defaults are 9050, 9051, and None respectively.
# If there is already a Tor process listening the specified
# ports, TorSession will use that one.
# Otherwise, it will create a new Tor process,
# and terminate it at the end.
with RotatingTorSession(proxy_port=9050, ctrl_port=9051,
                        password="MYSUPERSAFEPSWD") as session:
    for i in range(0, 5):
        try:
            response = session.get('https://ipecho.net/plain')
            print(response.text)  # not your IP address, different every time
        except KeyboardInterrupt:
            break
```

## Proxy Sources

Proxies are scrapped from the following websites

- http://free-proxy.cz
- https://free-proxy-list.net
- https://www.socks-proxy.net
- https://www.sslproxies.org
- https://www.us-proxy.org
- https://hidemy.name
- http://proxydb.net
- https://www.proxynova.com
- https://www.proxyscan.io
- http://pubproxy.com
- https://spys.me
- https://spys.one

## TODO

- import/export proxy list
- suggest more in github issues!