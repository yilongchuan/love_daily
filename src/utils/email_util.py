import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import List
import time

class EmailUtil:
    def __init__(self, config: dict):
        self.smtp_server = config['smtp_server']
        self.smtp_port = config['smtp_port']
        self.sender = config['sender']
        self.password = config['password']
        self.receivers = config['receivers']
        
    def _create_html_message(self, content: str) -> str:
        """创建HTML格式的邮件内容"""
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: #f5f5f5; font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                {content}
            </div>
        </body>
        </html>
        """
        return html

    def send_email(self, content: str, subject_content: str = None, max_retries: int = 3) -> bool:
        """
        发送邮件，支持重试机制
        :param content: 邮件内容
        :param subject_content: 邮件主题内容（情话）
        :param max_retries: 最大重试次数
        """
        server = None
        for attempt in range(max_retries):
            try:
                msg = MIMEMultipart()
                # 使用Header正确编码发件人名称
                sender_name = Header('EG', 'utf-8').encode()
                msg['From'] = f'{sender_name} <{self.sender}>'
                msg['To'] = ','.join(self.receivers)
                
                # 设置邮件主题
                if subject_content:
                    subject = f"早安宝贝！"
                else:
                    subject = f"今日问候 - {time.strftime('%Y-%m-%d')}"
                
                msg['Subject'] = Header(subject, 'utf-8')
                
                html_content = self._create_html_message(content)
                msg.attach(MIMEText(html_content, 'html', 'utf-8'))
                
                # 确保之前的连接已关闭
                if server:
                    try:
                        server.quit()
                    except:
                        pass
                
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.receivers, msg.as_string())
                server.quit()
                return True
                
            except Exception as e:
                print(f"第{attempt + 1}次尝试发送邮件失败: {str(e)}")
                if server:
                    try:
                        server.quit()
                    except:
                        pass
                
                if attempt < max_retries - 1:
                    print("等待2秒后重试...")
                    time.sleep(2)
                else:
                    print("已达到最大重试次数，发送失败")
                    return False
        
        return False 