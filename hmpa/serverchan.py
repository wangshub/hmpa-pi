import requests
import json

API_URL = "https://sc.ftqq.com/{sckey}.send"


def push(sckey, title, content=''):
    """push message to wechat

    :param sckey: serverchan sckey
    :param title: msg title (256B max)
    :param content: msg content (64kB max. support markdown)
    :return: response
    """
    url = API_URL.format(sckey=sckey)
    try:
        response = requests.post(url, data={"text": title, "desp": content})
        result = json.loads(response.text)
        return result
    except Exception as err:
        print(err)
        return None