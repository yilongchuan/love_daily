import requests
import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from utils.date_util import (get_love_days, get_birthday_countdown, format_date, 
                           is_birthday, get_birthday_wish, is_anniversary, 
                           get_anniversary_year, get_anniversary_wish)
from utils.weather_util import WeatherUtil
from utils.sweet_words_util import SweetWordsUtil

def load_config():
    with open('./src/config/config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def send_message(webhook_url: str, content: str):
    """发送消息到企业微信"""
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    response = requests.post(webhook_url, json=data)
    return response.json()

def job():
    """定时执行的任务"""
    config = load_config()
    webhook_url = config['basic']['webhook_url']
    
    # 初始化工具
    weather_util = WeatherUtil(config['weather']['key'])
    sweet_words_util = SweetWordsUtil()
    
    # 获取天气信息
    boy_weather = weather_util.get_weather(
        config['weather']['locations']['boy']['city'],
        config['weather']['locations']['boy']['district']
    )
    girl_weather = weather_util.get_weather(
        config['weather']['locations']['girl']['city'],
        config['weather']['locations']['girl']['district']
    )
    
    # 获取天气预警信息
    boy_warnings = weather_util.get_weather_warning(
        config['weather']['locations']['boy']['city'],
        config['weather']['locations']['boy']['district']
    )
    girl_warnings = weather_util.get_weather_warning(
        config['weather']['locations']['girl']['city'],
        config['weather']['locations']['girl']['district']
    )
    
    # 格式化天气预警信息
    boy_warning_text = weather_util.format_warning(boy_warnings)
    girl_warning_text = weather_util.format_warning(girl_warnings)
    
    # 构建天气预警消息
    warning_message = ""
    if boy_warning_text or girl_warning_text:
        warning_message = "\n⚠️ 天气预警提醒 ⚠️"
        if girl_warning_text:
            warning_message += f"\n青岛：\n{girl_warning_text}"
        if boy_warning_text:
            warning_message += f"\n上海：\n{boy_warning_text}"
        warning_message += "\n请注意防护，注意安全！❤️"
    
    # 获取日期相关信息
    love_days = get_love_days(config['personal']['anniversary'])
    boy_birth_days = get_birthday_countdown(config['personal']['birthdays']['boy'])
    girl_birth_days = get_birthday_countdown(config['personal']['birthdays']['girl'])
    
    # 检查是否是特殊日子
    boy_birthday = is_birthday(config['personal']['birthdays']['boy'])
    girl_birthday = is_birthday(config['personal']['birthdays']['girl'])
    is_anni = is_anniversary(config['personal']['anniversary'])
    
    # 构建特殊日子消息
    special_message = ""
    if boy_birthday:
        wish = get_birthday_wish(config['personal']['birthdays']['boy']['wishes'])
        special_message = f"\n\n🎉 亲爱的👦，生日快乐！🎂\n✨ {wish}"
    elif girl_birthday:
        wish = get_birthday_wish(config['personal']['birthdays']['girl']['wishes'])
        special_message = f"\n\n🎉 亲爱的👧，生日快乐！🎂\n✨ {wish}"
    elif is_anni:
        years = get_anniversary_year(config['personal']['anniversary'])
        wish = get_anniversary_wish(config['personal']['anniversary_wishes'], years)
        special_message = f"\n\n💝 {wish} 🎊"
    
    # 获取每日情话
    sweet_words = sweet_words_util.get_random_words()
    
    # 构建消息内容
    content = f"""🌅 早安呀！今天是我们在一起的第 {love_days} 天啦 💑

📅 今天是 {format_date()}

🌈 今日天气小贴士：
🏙️ 青岛：{weather_util.format_weather(girl_weather)}
🌆 上海：{weather_util.format_weather(boy_weather)}
{warning_message}

🎂 生日倒计时：
👧 生日还有 {girl_birth_days} 天
👦 生日还有 {boy_birth_days} 天
{special_message}
💌 今日情话：{sweet_words} """
    result = send_message(webhook_url, content)
    print(f"发送结果: {result}")

def main():
    job()

if __name__ == "__main__":
    main() 