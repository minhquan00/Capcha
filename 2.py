import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Danh sách API proxy HTTP/HTTPS
API_SOURCES = [
    "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=ipport&format=text&timeout=1500",
    "https://openproxy.space/list/http",
    "http://36.50.134.20:3000/download/http.txt",
    "http://36.50.134.20:3000/download/vn.txt",
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http",
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all',
    'https://api.proxifly.dev/proxies?protocol=http',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/https.txt',
    'https://www.proxy-list.download/api/v1/get?type=http',
    'https://www.proxy-list.download/api/v1/get?type=https',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http%2Chttps',
    'http://pubproxy.com/api/proxy?limit=20&format=txt&type=http',
    'https://www.freeproxy.world/?type=http&anonymity=elite',
    'https://gimmeproxy.com/api/getProxy?protocol=http',
    'http://free-proxy.cz/en/proxylist/main/export',
    'https://proxydb.net/api/proxies?protocol=http',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://www.proxy-list.download/api/v1/get?type=http',
        'https://api.openproxylist.xyz/http.txt',
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt',
        'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt',
        'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
        'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt',
        'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt',
        'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt',
        'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
        'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt',
        'https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt',
        'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
        'https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt',
        'https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt',
        'https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt',
        'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt'
        'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all',
]

def fetch_proxies_from_url(url):
    """Tải proxy từ một API."""
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            proxies = []
            lines = resp.text.strip().split('\n')
            for line in lines:
                # Chỉ lấy dòng có định dạng IP:Port
                if ':' in line and len(line.split(':')) == 2:
                    proxies.append(line.strip())
            print(f"Tải được {len(proxies)} proxy từ {url}")
            return proxies
    except Exception as e:
        print(f"Lỗi tải từ {url}: {e}")
    return []

def fetch_all_proxies(max_workers=10):
    """Tải proxy từ tất cả API (đa luồng)."""
    all_proxies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_proxies_from_url, url) for url in API_SOURCES]
        for future in as_completed(futures):
            proxies = future.result()
            all_proxies.extend(proxies)
    print(f"Tổng proxy tải được: {len(all_proxies)}")
    return all_proxies

if __name__ == "__main__":
    print("🚀 Tool tải proxy HTTP/HTTPS từ siêu nhiều API!")
    
    # Xóa file http.txt nếu đã tồn tại
    output_file = 'http.txt'
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"🗑️ Đã xóa file cũ: {output_file}")
    
    proxies = fetch_all_proxies()
    if proxies:
        with open(output_file, 'w') as f:
            f.write('\n'.join(proxies))
        print(f"\n💾 Lưu {len(proxies)} proxy vào file: {output_file}")
    else:
        print("❌ Không tải được proxy nào.")