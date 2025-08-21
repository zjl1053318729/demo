"""辅助函数"""
import logging
import streamlit as st
from typing import Any, Dict, Optional
from datetime import datetime

def setup_logging(level: str = "INFO"):
    """设置日志配置
    
    Args:
        level: 日志级别
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def handle_error(func):
    """错误处理装饰器
    
    Args:
        func: 被装饰的函数
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            st.error(f"操作失败: {str(e)}")
            return None
    return wrapper

def safe_get_session_state(key: str, default: Any = None) -> Any:
    """安全获取session state值
    
    Args:
        key: 键名
        default: 默认值
        
    Returns:
        session state中的值或默认值
    """
    return st.session_state.get(key, default)

def format_message_for_display(message: Dict[str, Any]) -> Dict[str, str]:
    """格式化消息用于显示
    
    Args:
        message: 原始消息数据
        
    Returns:
        格式化后的消息数据
    """
    return {
        'content': message.get('content', ''),
        'sender': message.get('sender', 'unknown'),
        'timestamp': format_datetime(message.get('timestamp', '')),
        'status': message.get('status', 'unknown')
    }

def format_datetime(timestamp_str: str) -> str:
    """格式化日期时间
    
    Args:
        timestamp_str: ISO格式的时间戳字符串
        
    Returns:
        格式化后的时间字符串
    """
    try:
        if isinstance(timestamp_str, str):
            dt = datetime.fromisoformat(timestamp_str)
        else:
            dt = timestamp_str
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "未知时间"

def truncate_text(text: str, max_length: int = 100) -> str:
    """截断文本
    
    Args:
        text: 原始文本
        max_length: 最大长度
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def validate_api_response(response: Dict[str, Any]) -> bool:
    """验证API响应
    
    Args:
        response: API响应数据
        
    Returns:
        是否有效
    """
    required_fields = ['success', 'content']
    return all(field in response for field in required_fields)

def create_error_message(error_type: str, details: str = "") -> Dict[str, Any]:
    """创建错误消息
    
    Args:
        error_type: 错误类型
        details: 错误详情
        
    Returns:
        错误消息字典
    """
    error_messages = {
        'api_error': '抱歉，AI服务暂时不可用，请稍后再试。',
        'network_error': '网络连接异常，请检查网络设置。',
        'timeout_error': '请求超时，请稍后再试。',
        'validation_error': '输入内容不符合要求，请检查后重试。',
        'unknown_error': '系统出现未知错误，请联系管理员。'
    }
    
    return {
        'success': False,
        'error': error_type,
        'content': error_messages.get(error_type, error_messages['unknown_error']),
        'details': details
    }

def log_user_action(action: str, details: Optional[Dict[str, Any]] = None):
    """记录用户操作
    
    Args:
        action: 操作类型
        details: 操作详情
    """
    logger = logging.getLogger('user_actions')
    log_data = {
        'action': action,
        'timestamp': datetime.now().isoformat(),
        'session_id': st.session_state.get('session_id', 'unknown'),
        'details': details or {}
    }
    logger.info(f"User action: {log_data}")

def generate_session_id() -> str:
    """生成会话ID
    
    Returns:
        会话ID
    """
    import uuid
    return str(uuid.uuid4())

def clean_text_input(text: str) -> str:
    """清理文本输入
    
    Args:
        text: 原始文本
        
    Returns:
        清理后的文本
    """
    if not text:
        return ""
    
    # 去除首尾空白
    text = text.strip()
    
    # 替换多个连续空格为单个空格
    import re
    text = re.sub(r'\s+', ' ', text)
    
    return text

def is_valid_message_content(content: str, max_length: int = 1000) -> tuple:
    """验证消息内容
    
    Args:
        content: 消息内容
        max_length: 最大长度
        
    Returns:
        (是否有效, 错误信息)
    """
    if not content or not content.strip():
        return False, "消息内容不能为空"
    
    if len(content) > max_length:
        return False, f"消息长度不能超过 {max_length} 个字符"
    
    return True, ""

def get_system_info() -> Dict[str, Any]:
    """获取系统信息
    
    Returns:
        系统信息字典
    """
    import platform
    import sys
    
    return {
        'platform': platform.system(),
        'python_version': sys.version,
        'streamlit_version': st.__version__,
        'timestamp': datetime.now().isoformat()
    }