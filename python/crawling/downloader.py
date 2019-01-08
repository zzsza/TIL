from random import choice
import requests

from throttle import Throttle


class Downloader:
    def __init__(self, delay=5, user_agent='wswp', proxies=None, cache={},
                 timeout=60):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.cache = cache
        self.num_retries = None  # we will set this per request
        self.timeout = timeout

    def __call__(self, url, num_retries=2):
        self.num_retries = num_retries
        try:
            result = self.cache[url]
            print('Loaded from cache:', url)
        except KeyError:
            result = None
        if result and self.num_retries and 500 <= result['code'] < 600:
            result = None
        if result is None:
            self.throttle.wait(url)
            proxies = choice(self.proxies) if self.proxies else None
            headers = {'User-Agent': self.user_agent}
            result = self.download(url, headers, proxies)
            self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxies):
        print('Downloading:', url)
        try:
            resp = requests.get(url, headers=headers, proxies=proxies,
                                timeout=self.timeout)
            html = resp.text
            if resp.status_code >= 400:
                print('Download error:', resp.text)
                html = None
                if self.num_retries and 500 <= resp.status_code < 600:
                    self.num_retries -= 1
                    return self.download(url, headers, proxies)
        except requests.exceptions.RequestException as e:
            print('Download error:', e)
            return {'html': None, 'code': 500}
        return {'html': html, 'code': resp.status_code}
