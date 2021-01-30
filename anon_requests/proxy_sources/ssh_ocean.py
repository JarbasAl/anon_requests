from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType
import bs4
import base64


class SSHOcean(ProxyGetter):
    url = 'https://sshocean.com/socks-proxy-list'

    def scrap_proxy_list(self):
        proxies = []
        page = self.session.get(self.url, headers=self.headers)
        doc = bs4.BeautifulSoup(page.text, features="html.parser")
        for el in doc.find_all("tr")[1:]:
            fields = [e.text for e in el.find_all("td")]
            if len(fields) < 8:
                continue
            ip = fields[0]
            port = fields[1]
            user = fields[5]
            password = fields[6]

            proxy_type = ProxyType.SOCKS5
            if fields[2] == "socks4":
                proxy_type = ProxyType.SOCKS4
            proxy_urls = {
                "http": f"{fields[2]}://{user}:{password}@" + ip + ":" + port,
                "https": f"{fields[2]}://{user}:{password}@" + ip + ":" + port
            }
            country_code = fields[3]  # TODO this is name + city, not code
            if fields[4] == "HIA":
                anon = ProxyAnonymity.ELITE
            elif fields[4] == "TODO":
                anon = ProxyAnonymity.ANONYMOUS
            else:
                anon = ProxyAnonymity.TRANSPARENT

            proxies.append({"ip": ip,
                            "port": port,
                            "username": user,
                            "password": password,
                            "country_code": country_code,
                            "proxy_anonymity": anon,
                            "proxy_type": proxy_type,
                            "urls": proxy_urls})

        return proxies
