"""营销文案生成服务"""
import requests
import asyncio
import logging
from typing import Dict, Any, Optional
from config.settings import DifyConfig

class MarketingService:
    """营销文案生成服务类"""
    
    def __init__(self, config: DifyConfig):
        self.config = config
        self.headers = {
            'Authorization': f'Bearer {config.api_key}',
            'Content-Type': 'application/json'
        }
        self.logger = logging.getLogger(__name__)
    
    async def generate_marketing_copy(self, prompt: str) -> Dict[str, Any]:
        """生成营销文案
        
        Args:
            prompt: 用户输入的完整提示词
            
        Returns:
            包含生成结果的字典
        """
        payload = {
            'inputs': {},
            'query': prompt,
            'response_mode': 'blocking',
            'user': 'marketing_user'
        }
        
        try:
            # 使用asyncio运行同步请求
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.post(
                    f"{self.config.base_url}/chat-messages",
                    headers=self.headers,
                    json=payload,
                    timeout=self.config.timeout
                )
            )
            
            response.raise_for_status()
            data = response.json()
            
            self.logger.info(f"营销文案生成成功，消息ID: {data.get('message_id')}")
            
            return {
                'success': True,
                'content': data.get('answer', ''),
                'message_id': data.get('message_id'),
                'usage': data.get('metadata', {}).get('usage', {})
            }
            
        except requests.exceptions.Timeout:
            error_msg = "文案生成超时，请稍后再试"
            self.logger.error(f"营销文案生成超时: {self.config.timeout}秒")
            return {
                'success': False,
                'error': 'timeout',
                'content': error_msg
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = "文案生成服务暂时不可用，请稍后再试"
            self.logger.error(f"营销文案生成API调用失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': error_msg
            }
            
        except Exception as e:
            error_msg = "系统出现错误，请联系管理员"
            self.logger.error(f"营销文案生成未知错误: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': error_msg
            }
    