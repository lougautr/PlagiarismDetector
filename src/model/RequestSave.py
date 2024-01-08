import requests

def requestAndSave(url):
    r = requests.get(url)

    print(url, r.status_code)
    print("-----------")
    if r.status_code == 200:
        return (True, r.content)

    return (False, None)
