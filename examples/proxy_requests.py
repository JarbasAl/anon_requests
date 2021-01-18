from anon_requests import ProxySession, NoMoreProxies, \
    ProxyType, ProxyAnonymity

with ProxySession(proxy_type=ProxyType.HTTPS,
                  proxy_anonymity=ProxyAnonymity.ELITE) as session:
    while True:
        try:
            response = session.get('https://ipecho.net/plain', timeout=5)
            if response.status_code == 200:
                print(response.text)  # not your IP address
            else:
                pass  # bad proxy
        except KeyboardInterrupt:
            break
        except Exception as e:
            #print("bad proxy, not working or very slow!")
            #print(session.current_proxy)
            #print(e)
            pass

        try:
            session.rotate_identity()  # new proxy
        except NoMoreProxies:
            print("used all available proxies")
            break
