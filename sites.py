import aiohttp
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class ProxySite(ABC):
    def __init__(self, url, is_api, params):
        self.site = None
        self.url = url
        self.is_api = is_api
        self.params = params

    async def parse(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as response:
                try:
                    if self.is_api:
                        self.site = await response.json()
                    else:
                        html = await response.text()
                        self.site = BeautifulSoup(html, "html.parser")
                except Exception as e:
                    print(f"Parse error: {e}")

    @classmethod
    async def create(cls, url, is_api, params=None):
        self = cls(url, is_api, params)
        await self.parse()
        return self

    @abstractmethod
    async def proxy_list(self):
        pass


class FreeProxyList(ProxySite):
    async def proxy_list(self):
        list_trs = self.site.find_all("tbody")[0].find_all("tr")
        proxies = []
        for tr in list_trs:
            cell = tr.find_all("td")
            ip = cell[0].get_text()
            port = cell[1].get_text()
            proxies.append(f"{ip}:{port}")

        return proxies


class Geonode(ProxySite):
    async def proxy_list(self):
        data = self.site.get("data")
        if data:
            proxies = []
            for proxy in data:
                try:
                    proxies.append(f"{proxy['ip']}:{proxy['port']}")
                except KeyError:
                    pass
            return proxies
