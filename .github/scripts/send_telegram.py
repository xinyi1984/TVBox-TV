import json
import requests
import os
import time

# 发送Telegram消息的函数
def send_telegram_message(bot_token, chat_id, text):
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML',  # 使用HTML格式
                'disable_web_page_preview': 'true'  # 改为true禁用链接预览
            },
            timeout=30
        )
        return response.status_code == 200
    except Exception as e:
        print(f"发送Telegram消息失败: {e}")
        return False

# 获取版本信息
try:
    # 获取电视版版本信息
    leanback_data = requests.get("https://raw.githubusercontent.com/FongMi/Release/fongmi/apk/release/leanback.json").json()
    tv_name = leanback_data.get('name', '未知版本')
    tv_desc = leanback_data.get('desc', '无更新日志')
    # 处理更新日志格式（从字符串转换为列表）
    tv_changelog = [item.strip() for item in tv_desc.split('\n') if item.strip()] if isinstance(tv_desc, str) else ['无详细更新日志']
except Exception as e:
    print(f"获取电视版信息失败: {e}")
    tv_name = "获取失败"
    tv_changelog = ["无法获取更新日志"]

try:
    # 获取手机版版本信息
    mobile_data = requests.get("https://raw.githubusercontent.com/FongMi/Release/fongmi/apk/release/mobile.json").json()
    mobile_name = mobile_data.get('name', '未知版本')
    mobile_desc = mobile_data.get('desc', '无更新日志')
    # 处理更新日志格式
    mobile_changelog = [item.strip() for item in mobile_desc.split('\n') if item.strip()] if isinstance(mobile_desc, str) else ['无详细更新日志']
except Exception as e:
    print(f"获取手机版信息失败: {e}")
    mobile_name = "获取失败"
    mobile_changelog = ["无法获取更新日志"]

# 电视版完整消息模板（使用HTML格式）
tv_full_message = f"""<b>TV正式版：</b>{tv_name}
<b><a href="https://github.com/FongMi/TV">影視</a>-<a href="https://github.com/FongMi/Release/tree/fongmi/apk">蜂蜜&唐三版</a>更新啦！</b>

<b>更新内容：</b>
{chr(10).join([f'* {item.strip("* ")}' for item in tv_changelog])}

<b><a href="https://t.me/tvb_ys">影視OK版</a> <a href="https://github.com/fongmi/release">APP库</a> <a href="https://github.com/FongMi/CatVodSpider">虫库</a></b>

<b><a href="https://t.me/tv_box_app">本频道</a> <a href="https://t.me/fongmi_official">影視群</a> <a href="https://t.me/TVBoxxoo">飯總群</a></b>

<b><a href="https://t.me/wangerxiaofangniuwa">牛娃群</a> <a href="https://t.me/okdespace">OK影视群</a></b>

Down🐝 :<a href="https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/leanback-armeabi_v7a.apk">32</a> <a href="https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/leanback-arm64_v8a.apk">64</a>     

下载🐝 :<a href="https://ghfast.top/https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/leanback-armeabi_v7a.apk">32</a> <a href="https://ghfast.top/https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/leanback-arm64_v8a.apk">64</a>     

線上接口推薦：
<a href="http://www.饭太硬.com/tv">飯總</a> <a href="https://100km.top/0">騷零</a> <a href="https://ghfast.top/https://raw.githubusercontent.com/FongMi/CatVodSpider/main/json/demo.json">蜂蜜</a> <a href="https://3450.kstore.space/DEMO.json">小米</a> <a href="http://肥猫.live/">肥猫</a>  

<a href="http://ok321.top/tv">OK佬1</a> <a href="http://ok321.top/ok">OK佬2</a> <a href="http://tvbox.王二小放牛娃.top/">牛娃</a> <a href="http://www.饭太硬.com/">更多</a>

本地接口包推薦：
<a href="https://www.123pan.com/s/alSeVv-lGO0A.html">香佬</a> <a href="https://t.me/watson1028">貓爪</a>

❓ 支持与帮助
<a href="https://t.me/fongmi_official">使用反饋</a> | <a href="https://paypal.me/fongmitw">打賞</a>"""

# 手机版完整消息模板（使用HTML格式）
mobile_full_message = f"""<b>手机/平板正式版：</b>{mobile_name}
<b><a href="https://github.com/FongMi/TV">影視</a>-<a href="https://github.com/FongMi/Release/tree/fongmi/apk">蜂蜜&唐三版</a>更新啦！</b>

<b>更新内容：</b>
{chr(10).join([f'* {item.strip("* ")}' for item in mobile_changelog])}

<b><a href="https://t.me/tvb_ys">影視OK版</a> <a href="https://github.com/fongmi/release">APP库</a> <a href="https://github.com/FongMi/CatVodSpider">虫库</a></b>

<b><a href="https://t.me/tv_box_app">本频道</a> <a href="https://t.me/fongmi_official">影視群</a> <a href="https://t.me/TVBoxxoo">飯總群</a></b>

<b><a href="https://t.me/wangerxiaofangniuwa">牛娃群</a> <a href="https://t.me/okdespace">OK影视群</a></b>

Down🐝 :<a href="https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/mobile-armeabi_v7a.apk">32</a> <a href="https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/mobile-arm64_v8a.apk">64</a>     

下载🐝 :<a href="https://ghfast.top/https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/mobile-armeabi_v7a.apk">32</a> <a href="https://ghfast.top/https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/mobile-arm64_v8a.apk">64</a>     

線上接口推薦：
<a href="http://www.饭太硬.com/tv">飯總</a> <a href="https://100km.top/0">騷零</a> <a href="https://ghfast.top/https://raw.githubusercontent.com/FongMi/CatVodSpider/main/json/demo.json">蜂蜜</a> <a href="https://3450.kstore.space/DEMO.json">小米</a> <a href="http://肥猫.live/">肥猫</a>  

<a href="http://ok321.top/tv">OK佬1</a> <a href="http://ok321.top/ok">OK佬2</a> <a href="http://tvbox.王二小放牛娃.top/">牛娃</a> <a href="http://www.饭太硬.com/">更多</a>

本地接口包推薦：
<a href="https://www.123pan.com/s/alSeVv-lGO0A.html">香佬</a> <a href="https://t.me/watson1028">貓爪</a>

❓ 支持与帮助
<a href="https://t.me/fongmi_official">使用反饋</a> | <a href="https://paypal.me/fongmitw">打賞</a>"""

# 发送消息到Telegram频道
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
channel_id = os.environ.get('TELEGRAM_CHANNEL_ID')

print("发送电视版完整消息...")
if send_telegram_message(bot_token, channel_id, tv_full_message):
    print("✅ 电视版完整消息发送成功")
else:
    print("❌ 电视版消息发送失败")

# 等待2秒避免发送过快被限制
time.sleep(2)

print("发送手机版完整消息...")
if send_telegram_message(bot_token, channel_id, mobile_full_message):
    print("✅ 手机版完整消息发送成功")
else:
    print("❌ 手机版消息发送失败")

print("完整格式通知发送完成！")
