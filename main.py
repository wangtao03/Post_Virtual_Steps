import datetime
import json
import os
import hashlib
import time
import urllib.parse

import requests

users = json.loads(os.environ['USERS'])
mobile = {
    "brand": os.environ['BRAND'],
    "model": os.environ['MODEL'],
    "version": os.environ['VERSION'],
    "deviceid": os.environ['DEVICE_ID']
}

def singGenerator(value: dict) -> str:
    text = '{' \
           f'"app_imei":"{value["app_imei"]}",' \
           f'"app_type":"{value["app_type"]}",' \
           f'"app_version":"{value["app_version"]}",' \
           f'"brand":"{value["brand"]}",' \
           f'"data_source":"{value["data_source"]}",' \
           f'"mHuaWeiStep":"{value["mHuaWeiStep"]}",' \
           f'"mPhoneServerStepIncreased":"{value["mPhoneServerStepIncreased"]}",' \
           f'"mPhoneStep":"{value["mPhoneStep"]}",' \
           f'"mServerStep":"{value["mServerStep"]}",' \
           f'"mTotalStep":"{value["mTotalStep"]}",' \
           f'"mWechatStep":"{value["mWechatStep"]}",' \
           f'"model":"{value["model"]}",' \
           f'"os_version":"{value["os_version"]}",' \
           f'"request_time":"{value["request_time"]}",' \
           f'"sport_type":"{value["sport_type"]}",' \
           f'"step_count":"{value["step_count"]}",' \
           f'"time_str":"{value["time_str"]}",' \
           f'"time_zone":"{value["time_zone"]}",' \
           f'"token":"{value["token"]}"' \
           '}willgoapi_beijing_api_key'

    md5 = hashlib.md5(text.encode("utf-8")).hexdigest()
    return md5


def getMaxSteps() -> int:
    timezone = datetime.timezone(datetime.timedelta(hours=8))
    hour = datetime.datetime.now(tz=timezone).hour
    if hour <= 7:
        return 19999
    elif hour == 8:
        return 25999
    elif 9 <= hour <= 13:
        return (hour - 4) * 6000 + 2000
    else:
        return 58000


class Sport:
    url = "https://capi.wewillpro.com/sport/addSportRecord"
    app_version = "2.8.1"  # APP版本

    def postSportRecord(self, token: str) -> bool:
        headers = {
            "Host": "capi.wewillpro.com",
            "appversion": self.app_version,
            "brand": mobile["brand"],
            "osversion": mobile["version"],
            "device_id": mobile["deviceid"],
            "content-type": "application/x-www-form-urlencoded",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/3.12.1"
        }

        maxSteps = getMaxSteps()
        timestamp = round(time.time())

        value = {
            "mServerStep": 0,
            "app_type": "1",
            "app_version": self.app_version,
            "mHuaWeiStep": "0",
            "os_version": mobile["version"],
            "step_count": maxSteps,
            "sign": "",
            "time_zone": "GMT+08:00",
            "mPhoneStep": maxSteps,
            "time_str": timestamp,
            "mTotalStep": maxSteps,
            "data_source": "1",
            "token": token,
            "app_imei": mobile["deviceid"],
            "request_time": timestamp,
            "model": mobile["model"],
            "brand": mobile["brand"],
            "mWechatStep": "0",
            "sport_type": "0",
            "mPhoneServerStepIncreased": "0"
        }
        value["sign"] = singGenerator(value)
        data = urllib.parse.urlencode(value)
        try:
            response = requests.post(self.url, data=data, headers=headers, allow_redirects=False, timeout=30)
            jsons = json.loads(response.content.decode("utf-8"))
            if jsons["code"] == 200:
                return True
            else:
                return False
        except ():
            return False


if __name__ == '__main__':
    server_datetime = datetime.datetime.now()
    timezone = datetime.timezone(datetime.timedelta(hours=8))
    beijing_datetime = datetime.datetime.now(tz=timezone)
    print(f"当地时间:\t{server_datetime.strftime('%Y年%m月%d日 %H时%M分%S秒')}")
    print(f"北京时间:\t{beijing_datetime.strftime('%Y年%m月%d日 %H时%M分%S秒')}")
    print(f"待达标: {len(users)}人")
    i = 0
    for user in users:
        i += 1
        print("%02d、%s: %s" % (i, user['name'], Sport().postSportRecord(user['token'])))
        time.sleep(1)
