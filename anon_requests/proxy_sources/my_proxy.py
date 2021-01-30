from anon_requests.proxy_sources import ProxyGetter, ProxyAnonymity, ProxyType
import bs4
import base64


class MyProxy(ProxyGetter):
    url = 'https://www.my-proxy.com/'

    def scrap_proxy_list(self):
        proxies = []
        for t in ["elite", "anonymous", "socks-4", "socks-5", "proxy"]:
            url = self.url + f"free-{t}-proxy.html"
            proxies += self._scrap_url(url)
        url = self.url + "free-proxy-list.html"
        proxies += self._scrap_url(url)
        for i in range(2, 10):
            url = self.url + f"free-proxy-list-{i}.html"
            proxies += self._scrap_url(url)
        return proxies

    def _scrap_url(self, url):
        proxies = []
        page = self.session.get(url, headers=self.headers)
        doc = bs4.BeautifulSoup(page.text, features="html.parser")
        el = doc.find("div", {"class": "list"})
        for e in str(el).split("<br/>"):
            e = e.replace('<div class="list">', "") \
                .replace('<div class="to-lock">', "").replace("</div>", "")
            if not e or e == "None":
                continue
            ip, port = e.split(":")
            country_code = None
            if "#" in port:
                port, country_code = port.split("#")
            proxy_urls = {
                "http": ip + ":" + port,
                "https": ip + ":" + port
            }
            anon = ProxyAnonymity.TRANSPARENT
            if "elite" in url:
                anon = ProxyAnonymity.ELITE
            elif "anonymous" in url:
                anon = ProxyAnonymity.ANONYMOUS

            proxy_type = ProxyType.HTTP
            if "socks-4" in url:
                proxy_type = ProxyType.SOCKS4
                anon = ProxyAnonymity.ELITE
                proxy_urls = {
                    "http": "socks4://" + ip + ":" + port,
                    "https": "socks4://" + ip + ":" + port
                }
            elif "socks-5" in url:
                proxy_type = ProxyType.SOCKS5
                anon = ProxyAnonymity.ELITE
                proxy_urls = {
                    "http": "socks5://" + ip + ":" + port,
                    "https": "socks5://" + ip + ":" + port
                }

            proxies.append({"ip": ip,
                            "port": port,
                            "country_code": country_code,
                            "proxy_anonymity": anon,
                            "proxy_type": proxy_type,
                            "urls": proxy_urls})

        return proxies



