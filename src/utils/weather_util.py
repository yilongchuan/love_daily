import requests
from typing import Dict, Optional

class WeatherUtil:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://devapi.qweather.com/v7"
        self.warning_levels = {
            "1": "蓝色",
            "2": "黄色",
            "3": "橙色",
            "4": "红色"
        }
    
    def get_location_id(self, city: str, district: str = None) -> Optional[str]:
        """获取城市/区域的location_id"""
        url = "https://geoapi.qweather.com/v2/city/lookup"
        params = {
            "key": self.api_key,
            "location": district or city,
            "adm": city
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data["code"] == "200" and data["location"]:
                return data["location"][0]["id"]
        except Exception as e:
            print(f"获取location_id失败: {e}")
        return None

    def get_weather(self, city: str, district: str = None) -> Dict:
        """获取天气信息"""
        location_id = self.get_location_id(city, district)
        if not location_id:
            return {"error": "获取城市ID失败"}
        
        # 获取当天天气预报
        url = f"{self.base_url}/weather/3d"
        params = {
            "key": self.api_key,
            "location": location_id
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data["code"] == "200":
                daily = data["daily"][0]  # 获取今天的天气预报
                return {
                    "tempMin": daily["tempMin"],
                    "tempMax": daily["tempMax"],
                    "textDay": daily["textDay"],
                    "windDirDay": daily["windDirDay"],
                    "windScaleDay": daily["windScaleDay"]
                }
        except Exception as e:
            print(f"获取天气失败: {e}")
        return {"error": "获取天气信息失败"}

    def format_weather(self, weather_data: Dict) -> str:
        """格式化天气信息"""
        if "error" in weather_data:
            return "天气获取失败"
        
        return (f"{weather_data['textDay']} {weather_data['tempMin']}℃~{weather_data['tempMax']}℃ "
                f"{weather_data['windDirDay']}{weather_data['windScaleDay']}级") 

    def get_weather_warning(self, city: str, district: str = None) -> Dict:
        """获取天气预警信息"""
        location_id = self.get_location_id(city, district)
        if not location_id:
            return {"error": "获取城市ID失败"}
        
        url = f"{self.base_url}/warning/now"
        params = {
            "key": self.api_key,
            "location": location_id
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data["code"] == "200" and data["warning"]:
                warnings = []
                for w in data["warning"]:
                    level = self.warning_levels.get(w["level"], w["level"])
                    warnings.append({
                        "title": w["title"],
                        "type": w["typeName"],
                        "level": level,
                        "text": w["text"]
                    })
                return warnings
        except Exception as e:
            print(f"获取天气预警失败: {e}")
        return []

    def format_warning(self, warnings: list) -> str:
        """格式化天气预警信息"""
        if not warnings:
            return ""
        
        warning_texts = []
        for w in warnings:
            if isinstance(w, dict) and "error" not in w:
                warning_texts.append(f"⚠️ {w['type']}{w['level']}预警")
        
        return "\n".join(warning_texts) if warning_texts else ""