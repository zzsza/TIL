import os
import json
import re
import zlib
	
from datetime import datetime, timedelta
from urllib.parse import urlsplit
	
	
class DiskCache:
    def __init__(self, cache_dir='../data/cache', max_len=255, compress=True,
             encoding='utf-8', expires=timedelta(days=30)):
        self.cache_dir = cache_dir
        self.max_len = max_len
        self.compress = compress
        self.encoding = encoding
        self.expires = expires
	
    def url_to_path(self, url):
        components = urlsplit(url)
        path = components.path
        if not path.endswith('/'):
            path += '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        filename = re.sub(r'[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        filename = '/'.join(seg[:self.max_len] for seg in filename.split('/'))
        return os.path.join(self.cache_dir, filename)
	
    def __getitem__(self, url):
        path = self.url_to_path(url)
        if os.path.exists(path):
            mode = ('rb' if self.compress else 'r')
            with open(path, mode) as fp:
                if self.compress:
                    data = zlib.decompress(fp.read()).decode(self.encoding)
                    data = json.loads(data)
                else:
                    data = json.load(fp)
            exp_date = data.get('expires')
            if exp_date and datetime.strptime(exp_date, '%Y-%m-%dT%H:%M:%S') <= datetime.utcnow():
                print('Cache expired!', exp_date)
                raise KeyError(url + ' has expired.')
            return data
        else:
            raise KeyError(url + ' does not exist')
	
    def __setitem__(self, url, result):
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        mode = ('wb' if self.compress else 'w')
        result['expires'] = (datetime.utcnow() + self.expires).isoformat(
            timespec='seconds')
        with open(path, mode) as fp:
            if self.compress:
                data = bytes(json.dumps(result), self.encoding)
                fp.write(zlib.compress(data))
            else:
                json.dump(result, fp)
