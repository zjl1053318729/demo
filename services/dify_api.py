"""Dify API服务"""
import requests
import asyncio
import logging
from typing import Dict, Any, Optional
from config.settings import DifyConfig

class DifyAPIService:
    """Dify API服务类"""
    
    def __init__(self, config: DifyConfig):
        self.config = config
        self.headers = {
            'Authorization': f'Bearer {config.api_key}',
            'Content-Type': 'application/json'
        }
        self.logger = logging.getLogger(__name__)
    
    async def chat_completion(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """异步调用Dify聊天API
        
        Args:
            message: 用户消息
            conversation_id: 会话ID（可选）
            
        Returns:
            包含响应结果的字典
        """
        payload = {
            'inputs': {},
            'query': message,
            'response_mode': 'blocking',
            'user': 'demo_user'
        }
        
        if conversation_id:
            payload['conversation_id'] = conversation_id
        
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
            
            self.logger.info(f"API调用成功，消息ID: {data.get('message_id')}")
            
            return {
                'success': True,
                'content': data.get('answer', ''),
                'conversation_id': data.get('conversation_id'),
                'message_id': data.get('message_id'),
                'usage': data.get('metadata', {}).get('usage', {})
            }
            
        except requests.exceptions.Timeout:
            error_msg = "API调用超时，请稍后再试"
            self.logger.error(f"API调用超时: {self.config.timeout}秒")
            return {
                'success': False,
                'error': 'timeout',
                'content': error_msg
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = "AI服务暂时不可用，请稍后再试"
            self.logger.error(f"API调用失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': error_msg
            }
            
        except Exception as e:
            error_msg = "系统出现错误，请联系管理员"
            self.logger.error(f"未知错误: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': error_msg
            }
    
    def test_connection(self) -> bool:
        """测试API连接
        
        Returns:
            连接是否成功
        """
        try:
            response = requests.get(
                f"{self.config.base_url}/info",
                headers={'Authorization': f'Bearer {self.config.api_key}'},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"连接测试失败: {e}")
            return False