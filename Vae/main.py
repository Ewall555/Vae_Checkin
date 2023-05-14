import os
import re
import argparse

from Vae import vae
from messageSender import MessageSender

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--cookie_string", type=str, required=True)

    args = parser.parse_args()
    cookie_string = args.cookie_string
    pushplus_token = os.environ.get("PUSHPLUS_TOKEN", None)
    serverChan_sendkey = os.environ.get("SERVERCHAN_SENDKEY", None)
    bark_deviceKey = os.environ.get("BARK_DEVICEKEY", None)
    wxpusher_apptoken = os.environ.get("WXPUSHER_APPTOKEN", None)
    wxpusher_uid = os.environ.get("WXPUSHER_UID", str)

    message_tokens = {
        "pushplus_token": pushplus_token,
        "serverChan_token": serverChan_sendkey,
        "bark_deviceKey": bark_deviceKey,
        "wxpusher_token": wxpusher_apptoken,
    }

    message_sender = MessageSender()
    cookie_string = cookie_string.split("&&")
    message_all = str()
    Checkin_Code = list()
    Status_Code = list()
    for idx, cookie in enumerate(cookie_string):
        print(f"【账号{idx + 1}】")
        message_all = f"{message_all}【账号{idx + 1}】:\n"
        Checkin_Status, Status_Status, message = vae(cookie)
        Checkin_Code.append(Checkin_Status)
        Status_Code.append(Status_Status)
        message_all = f"{message_all}{message}\n"

    if False not in Checkin_Code and Checkin_Code.count(True) + Checkin_Code.count(False) == len(Checkin_Code):
        title = "Vae+签到成功!"
    else:
        title = "Vae+签到失败!"
    message_all = f"{title}\n{message_all}"
    message_all = re.sub("\n+", "\n", message_all)
    if message_all.endswith("\n"):
        message_all = message_all[:-1]
    wxpusher_uid = wxpusher_uid.split("&&")
    for wxuid in wxpusher_uid:
        message_sender.send_all(message_tokens=message_tokens, title=title, content=message_all, wxpusher_uid=wxuid)
    assert False not in Status_Code, "查询签到状态失败，请尝试更换Cookie。"
    assert Status_Code.count(True) + Status_Code.count(False) == len(Status_Code), "不是所有的账号Cookie都有效。"
