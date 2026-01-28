import requests as rp
import json

def get_data(url):
    res = rp.get(url)
    print(f"Response Status: {res.status_code}")
    data = json.loads(res.text)
    print(data)

if __name__ == '__main__':
    get_data('https://randomuser.me/api/')