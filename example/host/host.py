import time
import json
import random
import requests
from ping3 import verbose_ping

if __name__ == '__main__':
    while(True):
        data = json.load(open('data.json'))

        requests.get(url=data["url"], proxies=dict(http=random.choice([None, data["proxy"]])))

        verbose_ping(random.choice(data["hosts"]))

        time.sleep(random.uniform(0.5,1.5))