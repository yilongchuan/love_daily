import random
from pathlib import Path

class SweetWordsUtil:
    def __init__(self, file_path: str = './src/config/sweet_words.txt'):
        self.file_path = file_path
        self.words = self._load_words()
    
    def _load_words(self) -> list:
        """加载情话数据"""
        words = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        words.append(line)
        except Exception as e:
            print(f"加载情话文件失败: {e}")
            words = ["我爱你"]  # 默认情话
        return words
    
    def get_random_words(self) -> str:
        """随机获取一句情话"""
        return random.choice(self.words) 