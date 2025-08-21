"""应用配置管理"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

@dataclass
class DifyConfig:
    """Dify API配置"""
    api_key: str
    base_url: str
    timeout: int = 30
    
    @classmethod
    def from_env(cls):
        """从环境变量加载配置"""
        api_key = os.getenv('DIFY_API_KEY', '')
        if not api_key:
            raise ValueError("DIFY_API_KEY环境变量未设置")
        
        return cls(
            api_key=api_key,
            base_url=os.getenv('DIFY_BASE_URL', 'https://api.dify.ai/v1'),
            timeout=int(os.getenv('DIFY_TIMEOUT', '30'))
        )
    
    def validate(self):
        """验证配置"""
        if not self.api_key:
            raise ValueError("Dify API密钥不能为空")
        if not self.base_url:
            raise ValueError("Dify API基础URL不能为空")
        if self.timeout <= 0:
            raise ValueError("超时时间必须大于0")

@dataclass
class AppConfig:
    """应用配置"""
    title: str = "🚀 AI营销助手 - 客服对话 & 文案生成"
    page_icon: str = "🚀"
    layout: str = "wide"
    max_message_length: int = 1000
    debug: bool = False
    log_level: str = "INFO"
    
    dify: Optional[DifyConfig] = None
    
    @classmethod
    def load(cls):
        """加载完整配置"""
        config = cls(
            debug=os.getenv('APP_DEBUG', 'false').lower() == 'true',
            log_level=os.getenv('LOG_LEVEL', 'INFO')
        )
        config.dify = DifyConfig.from_env()
        config.dify.validate()
        return config