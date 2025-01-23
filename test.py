import requests
from utils.email_util import EmailUtil
import yaml

# 配置参数
app_id = "wx1de52bead2bba8d5"
app_secret = "d6c7d19f15ce2e6b1aaeb07ab97807c0"
openid = "o8Rg-6_eo13qymNL-9Ghb87oMa7g"
template_id = "hybv0ZGnLYj_By2UC1JIDbAlY_aVeYM_Omjbq-Y8D5o"

# 获取access_token
token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
token_response = requests.get(token_url)
access_token = token_response.json()['access_token']

# 发送模板消息
send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"

data = {
    "touser": openid,
    "template_id": template_id,
    "data": {
        "first": {
            "value": "🌅 早安呀！",
            "color": "#173177"
        },
        "love_days": {
            "value": "75",
            "color": "#FF0000"
        },
        "date": {
            "value": "2024年12月18日 (冬月十八)",
            "color": "#173177"
        },
        "weather": {
            "value": "青岛：晴 -1℃~2℃ 北风3-4级\n上海：晴 0℃~9℃ 北风1-3级",
            "color": "#173177"
        },
        "birthday": {
            "value": "👧 生日还有 75 天\n👦 生日还有 372 天",
            "color": "#173177"
        },
        "remark": {
            "value": "💌 喜欢你，就像小猫喜欢晒太阳一样自然",
            "color": "#173177"
        }
    }
}

response = requests.post(send_url, json=data)
print(response.json())

def test_email():
    with open('./src/config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    email_util = EmailUtil(config['email'])
    content = """
    <div style="color: #333;">
        <h1>测试邮件</h1>
        <p>如果你收到这封邮件，说明邮件配置成功了！</p>
    </div>
    """
    
    result = email_util.send_email(content)
    print("邮件发送成功" if result else "邮件发送失败")

if __name__ == "__main__":
    test_email()