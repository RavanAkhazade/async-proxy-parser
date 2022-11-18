import asyncio
from sites import FreeProxyList, Geonode
from checker import check, http_proxies, socks5_proxies


async def main():
    all_proxy_sites = [
        await FreeProxyList.create("https://free-proxy-list.net/", False),
        await Geonode.create("https://proxylist.geonode.com/api/proxy-list", True, {
            "limit": 500,
            "page": 1,
            "sort_by": "speed",
            "sort_type": "asc",
            "google": "true",
        })
    ]

    all_proxies = []
    for proxy_site in all_proxy_sites:
        all_proxies += await proxy_site.proxy_list()

    await asyncio.gather(*[check(proxy) for proxy in all_proxies])

    with open("http_proxies.txt", "w") as hf:
        for proxy in list(set(http_proxies)):
            hf.write(proxy + "\n")

    with open("socks5_proxies.txt", "w") as sf:
        for proxy in list(set(socks5_proxies)):
            sf.write(proxy + "\n")


loop = asyncio.get_event_loop()
w = loop.run_until_complete(main())
