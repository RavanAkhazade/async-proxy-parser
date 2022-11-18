import aiohttp
import yaml

with open("config.yaml", "r") as stream:
    try:
        data = yaml.safe_load(stream)
        check_url = data['check_url']
        headers = data['headers']
        timeout = data['timeout']
    except Exception as e:
        print(f"Config error: {e}")

http_proxies, socks5_proxies = [], []


async def check(proxy):
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(check_url, proxy=f"http://{proxy}", timeout=timeout):
                http_proxies.append(proxy)
            async with session.get(check_url, proxy=f"socks5://{proxy}", timeout=timeout):
                socks5_proxies.append(proxy)
    except Exception:
        return
