from datetime import datetime, date, time
from lunar_python import Lunar, Solar
import random

def get_love_days(anniversary: str) -> int:
    """计算恋爱天数"""
    start_date = datetime.strptime(anniversary, '%Y-%m-%d').date()
    today = date.today()
    return (today - start_date).days

def get_birthday_countdown(birthday_config: dict) -> int:
    """计算到下一个生日的天数"""
    today = date.today()
    
    # 解析生日配置
    birth_type = birthday_config['type']
    birth_date = datetime.strptime(birthday_config['date'], '%Y-%m-%d')
    
    if birth_type == 'lunar':
        # 农历生日，只取月和日
        lunar_birth = Lunar.fromYmd(today.year, birth_date.month, birth_date.day)
        # 获取今年的农历生日对应的阳历日期
        this_year_birth = lunar_birth.getSolar()
        
        # 转换为date对象
        birthday_this_year = date(
            this_year_birth.getYear(),
            this_year_birth.getMonth(),
            this_year_birth.getDay()
        )
        
        # 如果今年的已经过了，使用明年的日期
        if birthday_this_year < today:
            next_lunar = Lunar.fromYmd(today.year + 1, birth_date.month, birth_date.day)
            next_solar = next_lunar.getSolar()
            birthday_this_year = date(
                next_solar.getYear(),
                next_solar.getMonth(),
                next_solar.getDay()
            )
    else:
        # 阳历生日，只取月和日
        birthday_this_year = date(today.year, birth_date.month, birth_date.day)
        if birthday_this_year < today:
            birthday_this_year = date(today.year + 1, birth_date.month, birth_date.day)
    
    # 计算天数差
    days = (birthday_this_year - today).days
    return days

def format_date(dt: datetime = None) -> str:
    """格式化日期，同时显示农历日期"""
    if dt is None:
        dt = datetime.now()
    
    # 获取农历日期
    lunar = Lunar.fromDate(dt)
    lunar_str = f"{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
    
    return f"{dt.strftime('%Y年%m月%d日')} ({lunar_str})" 

def is_birthday(birthday_config: dict) -> bool:
    """判断今天是否是生日"""
    return get_birthday_countdown(birthday_config) == 0

def get_birthday_wish(wishes: list) -> str:
    """随机获取一条生日祝福"""
    return random.choice(wishes) 

def is_anniversary(anniversary: str) -> bool:
    """判断今天是否是周年纪念日"""
    start_date = datetime.strptime(anniversary, '%Y-%m-%d').date()
    today = date.today()
    return today.month == start_date.month and today.day == start_date.day

def get_anniversary_year(anniversary: str) -> int:
    """获取周年数"""
    start_date = datetime.strptime(anniversary, '%Y-%m-%d').date()
    today = date.today()
    years = today.year - start_date.year
    # 如果今年的纪念日还没到，年数减1
    if today.month < start_date.month or (today.month == start_date.month and today.day < start_date.day):
        years -= 1
    return years

def get_anniversary_wish(wishes: list, years: int) -> str:
    """获取周年纪念日祝福语"""
    wish = random.choice(wishes)
    return wish.format(count=years) 