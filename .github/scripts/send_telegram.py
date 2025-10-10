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
                'parse_mode': 'Markdown',
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

# 电视版完整消息模板
tv_full_message = f"""*TV正式版：{tv_name}*
[影視](https://github.com/FongMi/TV)-[蜂蜜&唐三版](https://github.com/FongMi/Release/tree/fongmi/apk)更新啦！

*更新内容：*
{chr(10).join([f'• {item.strip("* ")}' for item in tv_changelog])}

[影視OK版](https://t.me/tvb_ys) [APP库](https://github.com/fongmi/release) [虫库](https://github.com/FongMi/CatVodSpider)

[本频道](https://t.me/tv_box_app) [影視群](https://t.me/fongmi_official) [飯總群](https://t.me/TVBoxxoo) 

[牛娃群](https://t.me/wangerxiaofangniuwa) [OK影视群](https://t.me/okdespace)

*Down🐝* :[32](https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/leanback-armeabi_v7a.apk) [64](https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/leanback-arm64_v8a.apk)     

*下载🐝* :[32](https://ghfast.top/https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/leanback-armeabi_v7a.apk) [64](https://ghfast.top/https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/leanback-arm64_v8a.apk)     

*線上接口推薦：*
[飯總](http://www.饭太硬.com/tv) [騷零](https://100km.top/0) [蜂蜜](https://ghfast.top/https://raw.githubusercontent.com/FongMi/CatVodSpider/main/json/demo.json) [小米](https://3450.kstore.space/DEMO.json) [肥猫](http://肥猫.live/)  

[OK佬1](http://ok321.top/tv) [OK佬2](http://ok321.top/ok) [牛娃](http://tvbox.王二小放牛娃.top/) [更多](http://www.饭太硬.com/)

*本地接口包推薦：*
[香佬](https://www.123pan.com/s/alSeVv-lGO0A.html) [貓爪](https://t.me/watson1028)

*❓ 支持与帮助*
[使用反饋](https://t.me/fongmi_offical) | [打賞](https://paypal.me/fongmitw)"""

# 手机版完整消息模板
mobile_full_message = f"""*手机版：{mobile_name}*
[影視](https://github.com/FongMi/TV)-[蜂蜜&唐三版](https://github.com/FongMi/Release/tree/fongmi/apk)更新啦！

*更新内容：*
{chr(10).join([f'• {item.strip("* ")}' for item in mobile_changelog])}

[影視OK版](https://t.me/tvb_ys) [APP库](https://github.com/fongmi/release) [虫库](https://github.com/FongMi/CatVodSpider)

[本频道](https://t.me/tv_box_app) [影視群](https://t.me/fongmi_official) [飯總群](https://t.me/TVBoxxoo) 

[牛娃群](https://t.me/wangerxiaofangniuwa) [OK影视群](https://t.me/okdespace)

*Down🐝* :[32](https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/mobile-armeabi_v7a.apk) [64](https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/mobile-arm64_v8a.apk)     

*下载🐝* :[32](https://ghfast.top/https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/mobile-armeabi_v7a.apk) [64](https://ghfast.top/https://raw.githubusercontent.com/xinyi1984/TVBox-TV/fongmi/apk/release/mobile-arm64_v8a.apk)     

*線上接口推薦：*
[飯總](http://www.饭太硬.com/tv) [騷零](https://100km.top/0) [蜂蜜](https://ghfast.top/https://raw.githubusercontent.com/FongMi/CatVodSpider/main/json/demo.json) [小米](https://3450.kstore.space/DEMO.json) [肥猫](http://肥猫.live/)  

[OK佬1](http://ok321.top/tv) [OK佬2](http://ok321.top/ok) [牛娃](http://tvbox.王二小放牛娃.top/) [更多](http://www.饭太硬.com/)

*本地接口包推薦：*
[香佬](https://www.123pan.com/s/alSeVv-lGO0A.html) [貓爪](https://t.me/watson1028)

*❓ 支持与帮助*
[使用反饋](https://t.me/fongmi_offical) | [打賞](https://paypal.me/fongmitw)"""

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
