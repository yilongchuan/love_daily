import requests
import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from utils.date_util import (get_love_days, get_birthday_countdown, format_date, 
                           is_birthday, get_birthday_wish, is_anniversary, 
                           get_anniversary_year, get_anniversary_wish)
from utils.weather_util import WeatherUtil
from utils.sweet_words_util import SweetWordsUtil
from utils.email_util import EmailUtil
import os

def load_config():
    with open('./src/config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 从环境变量加载敏感信息
    if 'EMAIL_PASSWORD' in os.environ:
        config['email']['password'] = os.environ['EMAIL_PASSWORD']
    if 'EMAIL_SENDER' in os.environ:
        config['email']['sender'] = os.environ['EMAIL_SENDER']
    if 'EMAIL_RECEIVER' in os.environ:
        # 将逗号分隔的邮箱字符串转换为列表
        receivers = [email.strip() for email in os.environ['EMAIL_RECEIVER'].split(',')]
        config['email']['receivers'] = receivers
    if 'WEATHER_API_KEY' in os.environ:
        config['weather']['key'] = os.environ['WEATHER_API_KEY']
    
    return config

def send_message(content: str, subject_content: str = None) -> bool:
    """发送邮件消息"""
    config = load_config()
    email_util = EmailUtil(config['email'])
    return email_util.send_email(content, subject_content)

def job():
    """定时执行的任务"""
    try:
        config = load_config()
        
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
        content = f"""
        <div style="line-height: 1.6;">
            <h2 style="color: #333;">🌅 早安呀！今天是我们在一起的第 {love_days} 天啦 💑</h2>
            
            <p style="font-size: 16px;">📅 今天是 {format_date()}</p>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3 style="color: #333;">🌈 今日天气小贴士：</h3>
                <p>🏙️ 青岛：{weather_util.format_weather(girl_weather)}</p>
                <p>🌆 上海：{weather_util.format_weather(boy_weather)}</p>
                {warning_message}
            </div>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3 style="color: #333;">🎂 生日倒计时：</h3>
                <p>👧 生日还有 {girl_birth_days} 天</p>
                <p>👦 生日还有 {boy_birth_days} 天</p>
            </div>
            
            {special_message}
            
            <div style="background-color: #fff5f5; padding: 20px; border-radius: 10px; margin: 25px 0; border: 2px solid #ffcdd2;">
                <h3 style="color: #e57373; margin-top: 0;">💌 今日情话</h3>
                <p style="font-size: 18px; color: #ff4081; line-height: 1.8; margin: 10px 0 0 0; text-align: center; font-style: italic;">
                    {sweet_words}
                </p>
            </div>
        </div>
        """
        
        # 发送邮件，使用情话作为标题
        result = send_message(content, sweet_words)
        print("邮件发送成功" if result else "邮件发送失败")
        
    except Exception as e:
        print(f"执行任务时出现错误: {str(e)}")

def main():
    job()

if __name__ == "__main__":
    main() 