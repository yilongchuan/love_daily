# 每日情侣消息推送服务设计文档

## 1. 项目概述
一个基于Python FastAPI的自动化服务,通过企业微信机器人每天定时向情侣群发送包含天气、纪念日等信息的暖心消息。

### 1.1 环境要求
- Python 3.8+
- pip
- Windows系统

### 1.2 使用说明
1. 安装依赖: `pip install -r requirements.txt`
2. 修改配置文件 `config.yaml`
3. 编辑情话文件 `sweet_words.txt`
4. 双击 `start.bat` 启动程序

## 2. 核心功能
- 定时发送: 每天早上8:30自动推送消息
- 天气查询: 获取双方所在城市的天气信息
- 日期计算: 计算恋爱天数、生日倒计时
- 情话推送: 随机发送温馨情话

## 3. 项目结构
project/
├── src/
│   ├── main.py            # 主程序入口
│   ├── config/
│   │   ├── config.yaml    # 配置文件
│   │   └── sweet_words.txt# 情话数据(每行一条)
│   └── utils/
│       ├── date_util.py   # 日期计算工具
│       ├── weather_util.py# 天气查询工具
│       └── message_util.py# 消息发送工具
├── requirements.txt       # 依赖管理
├── start.bat             # 启动脚本
└── README.md             # 项目说明

+## 4. 配置文件说明
+### 4.1 config.yaml
+```yaml
+# 基础配置
+basic:
+  webhook_url: "企业微信机器人webhook地址"
+  weather_key: "和风天气API密钥"
+  send_time: "8:30"
+
+# 个人信息
+personal:
+  anniversary: "2023-01-01"  # 恋爱纪念日
+  birthdays:
+    boy: "1990-01-01"
+    girl: "1990-06-01"
+  locations:
+    boy: 
+      city: "上海"
+      district: "闵行"
+    girl:
+      city: "青岛"
+      district: "市北"
+
+# 消息模板
+message_template: |
+  今天是我们在一起的第 {love_days} 天 💑
+  
+  今天是 {date}
+  距离男生生日还有 {boy_birthday_count} 天
+  距离女生生日还有 {girl_birthday_count} 天
+  
+  今天天气:
+  {boy_name}所在的{boy_location}: {boy_weather}
+  {girl_name}所在的{girl_location}: {girl_weather}
+  
+  今日情话: {sweet_words}
+  
+  愿今天也是美好的一天 ❤️
+```
+
+### 4.2 sweet_words.txt
+```text
+# 情话文件格式说明:
+# 1. 每行一条情话
+# 2. 空行会被忽略
+# 3. #开头的行为注释,会被忽略
+# 4. 文件使用UTF-8编码
+
+# 示例情话
+我喜欢你,就像老鼠喜欢大米
+你是我这一生最美的桃花劫
+我的眼里只有你,就像蜜蜂眼里只有花蜜
+# 这条情话暂时不想用了
+#遇见你是我所有美好故事的开始
+```
+
+## 5. 后续扩展计划
+- 支持多种消息模板随机选择
+- 节日特殊消息提醒
+- 添加更多实用信息(如星座运势等)