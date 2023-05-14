import requests
import json


class MessageSender:
    def __init__(self):
        self.sender = {}

        self.register("pushplus_token", self.pushplus)
        self.register("serverChan_token", self.serverChan)
        self.register("bark_deviceKey", self.bark)
        self.register("wxpusher_token", self.wxpusher)

    def register(self, token_name, callback):
        assert token_name not in self.sender, "Register fails, the token name exists."
        self.sender[token_name] = callback

    def send_all(self, message_tokens, title, content, wxpusher_uid):
        def check_valid_token(token):
            if isinstance(token, type(None)):
                return False
            if isinstance(token, str) and len(token) == 0:
                return False
            if isinstance(token, list) and (token.count(None) != 0 or token.count("") != 0):
                return False
            return True

        for token_key in message_tokens:
            token_value = message_tokens[token_key]
            if token_key in self.sender and check_valid_token(token_value):
                try:
                    self.sender[token_key](token_value, title, content, wxpusher_uid)
                except Exception:
                    print(f"【Sender】Something wrong happened when handle {self.sender[token_key]}")

    @staticmethod
    def pushplus(token, title, content, wxpusher_uid):
        assert type(token) == str, "Wrong type for pushplus token."
        content = content.replace("\n", "\n\n")
        payload = {
            'token': token,
            "title": title,
            "content": content,
            "channel": "wechat",
            "template": "markdown"
        }
        resp = requests.post("http://www.pushplus.plus/send", data=payload)
        resp_json = resp.json()
        if resp_json["code"] == 200:
            print(f"【Pushplus】Send message to Pushplus successfully.")
        if resp_json["code"] != 200:
            print(f"【Pushplus】【Send Message Response】{resp.text}")
            return -1
        return 0

    @staticmethod
    def serverChan(sendkey, title, content, wxpusher_uid):
        assert type(sendkey) == str, "Wrong type for serverChan token."
        content = content.replace("\n", "\n\n")
        payload = {
            "title": title,
            "desp": content,
        }
        resp = requests.post(f"https://sctapi.ftqq.com/{sendkey}.send", data=payload)
        resp_json = resp.json()
        if resp_json["code"] == 0:
            print(f"【ServerChan】Send message to ServerChan successfully.")
        if resp_json["code"] != 0:
            print(f"【ServerChan】【Send Message Response】{resp.text}")
            return -1
        return 0

    @staticmethod
    def bark(device_key, title, content, wxpusher_uid):
        assert type(device_key) == str, "Wrong type for bark token."

        url = "https://api.day.app/push"
        headers = {
            "content-type": "application/json",
            "charset": "utf-8"
        }
        data = {
            "title": title,
            "body": content,
            "device_key": device_key
        }

        resp = requests.post(url, headers=headers, data=json.dumps(data))
        resp_json = resp.json()
        if resp_json["code"] == 200:
            print(f"【Bark】Send message to Bark successfully.")
        if resp_json["code"] != 200:
            print(f"【Bark】【Send Message Response】{resp.text}")
            return -1
        return 0

    @staticmethod
    def wxpusher(apptoken, title, content, wxpusher_uid):
        assert type(apptoken) == str, "Wrong type for wxpuhser token."
        content = content.replace("\n", "\n\n")
        headers = {
            'Content-Type': "application/json"
        }
        payload = {
            "appToken": apptoken,
            "content": content,
            "contentType": 3,
            "uids": [wxpusher_uid]
        }
        resp = requests.post(f"https://wxpusher.zjiecode.com/api/send/message", headers=headers,
                             data=json.dumps(payload))
        resp_json = resp.json()
        if resp_json["code"] == 0:
            print(f"【wxpusher】Send message to wxpusher successfully.")
        if resp_json["code"] != 0:
            print(f"【wxpusher】【Send Message Response】{resp.text}")
            return -1
        return 0
