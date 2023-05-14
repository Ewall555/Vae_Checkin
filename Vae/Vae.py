# encoding=utf8
import io
import sys
import json
import requests
import datetime


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def server_time(servertime):
    china_timezone = datetime.timezone(datetime.timedelta(hours=8))
    dt = datetime.datetime.fromtimestamp(servertime, china_timezone)
    date_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    return date_str


def vae_checkin(cookie_string):
    headers = {'Cookie': cookie_string}
    checkin_url = "http://api1-xusong.91q.com/USER_HOME/addRecord"
    response = requests.post(checkin_url, headers=headers)
    resp = json.loads(response.text)
    if resp["state"]:
        return resp["state"], resp["animation"]["title"]
    return resp["state"], resp["errMsg"]


def vae_status(cookie_string):
    headers = {'Cookie': cookie_string}
    status_url = "http://api1-xusong.91q.com/USER_HOME/getRecord"
    response = requests.post(status_url, headers=headers)
    resp = json.loads(response.text)
    if resp["state"]:
        return resp["state"], resp["result"]["signRecord"]["continuity"], resp["result"]["signRecord"]["totalCount"], \
               resp["result"]["signRecord"]["signToday"], resp["result"]["signRecord"]["rank"], resp["serverTime"]
    return resp["state"], resp["errMsg"], resp["serverTime"]


def vae(cookie_string):
    message = str()
    # 签到
    Checkin_Status, Checkin_Message = vae_checkin(cookie_string)
    message = f"{message}【签到】\n*{Checkin_Message}\n"
    print(f"【签到】\n*{Checkin_Message}")
    # 查询签到
    Status_Message = vae_status(cookie_string)
    if Status_Message[0]:
        Status_Status, Checkin_continuity, Checkin_totalCount, Checkin_signToday, Checkin_rank, Checkin_serverTime = Status_Message
        # 判断排名
        if Checkin_rank > 100 or Checkin_rank == 0:
            Checkin_rank = "未进入排行榜"
        else:
            Checkin_rank = f"第{Checkin_rank}名"
        # 判断签到状态
        if Checkin_signToday:
            Checkin_signToday = "已签到"
        else:
            Checkin_signToday = "未签到"
        Time = server_time(Checkin_serverTime)
        message = f"{message}【状态】\n*日期：{Time}\n*签到状态：{Checkin_signToday}\n*连续签到：{Checkin_continuity}天\n*总签到数：{Checkin_totalCount}天\n*今日排名：{Checkin_rank}\n"
        print(f"【状态】\n*日期：{Time}\n*签到状态：{Checkin_signToday}\n*连续签到：{Checkin_continuity}天\n*总签到数：{Checkin_totalCount}天\n*今日排名：{Checkin_rank}")
    else:
        Status_Status, Status_errMessage, Checkin_serverTime = Status_Message
        Time = server_time(Checkin_serverTime)
        message = f"{message}【状态】\n*日期：{Time}\n*状态：{Status_Status}{Time}\n*日志：{Status_errMessage}"
        print(f"【状态】\n*日期：{Time}\n*状态：{Status_Status}\n*日志：{Status_errMessage}")
    return Checkin_Status, Status_Status, message
