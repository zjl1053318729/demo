"""状态管理服务"""
import streamlit as st
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class Message:
    """消息数据类"""
    id: str
    content: str
    sender: str  # 'user', 'assistant', 'system'
    timestamp: datetime
    status: str  # 'sent', 'pending', 'failed'
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """从字典创建消息"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

@dataclass
class PendingReview:
    """待审核消息数据类"""
    id: str
    original_content: str
    edited_content: str
    timestamp: datetime
    user_message_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PendingReview':
        """从字典创建待审核消息"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

class StateManager:
    """状态管理器"""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """初始化会话状态"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'pending_review' not in st.session_state:
            st.session_state.pending_review = None
        if 'typing_status' not in st.session_state:
            st.session_state.typing_status = False
        if 'conversation_id' not in st.session_state:
            st.session_state.conversation_id = None
        if 'api_connected' not in st.session_state:
            st.session_state.api_connected = False
    
    def add_user_message(self, content: str) -> Message:
        """添加用户消息
        
        Args:
            content: 消息内容
            
        Returns:
            创建的消息对象
        """
        message = Message(
            id=str(uuid.uuid4()),
            content=content,
            sender='user',
            timestamp=datetime.now(),
            status='sent'
        )
        st.session_state.messages.append(message.to_dict())
        return message
    
    def set_typing_status(self, status: bool):
        """设置输入状态
        
        Args:
            status: 是否正在输入
        """
        st.session_state.typing_status = status
    
    def set_pending_review(self, content: str, user_message_id: str) -> PendingReview:
        """设置待审核消息
        
        Args:
            content: AI生成的内容
            user_message_id: 对应的用户消息ID
            
        Returns:
            创建的待审核消息对象
        """
        pending = PendingReview(
            id=str(uuid.uuid4()),
            original_content=content,
            edited_content=content,
            timestamp=datetime.now(),
            user_message_id=user_message_id
        )
        st.session_state.pending_review = pending.to_dict()
        return pending
    
    def update_pending_content(self, content: str):
        """更新待审核消息的编辑内容
        
        Args:
            content: 编辑后的内容
        """
        if st.session_state.pending_review:
            st.session_state.pending_review['edited_content'] = content
    
    def approve_message(self, final_content: Optional[str] = None) -> Optional[Message]:
        """批准并发送消息
        
        Args:
            final_content: 最终内容（如果为None则使用编辑后的内容）
            
        Returns:
            创建的消息对象
        """
        if not st.session_state.pending_review:
            return None
        
        content = final_content or st.session_state.pending_review['edited_content']
        
        message = Message(
            id=st.session_state.pending_review['id'],
            content=content,
            sender='assistant',
            timestamp=datetime.now(),
            status='sent'
        )
        
        st.session_state.messages.append(message.to_dict())
        st.session_state.pending_review = None
        st.session_state.typing_status = False
        
        return message
    
    def reject_message(self):
        """拒绝消息"""
        st.session_state.pending_review = None
        st.session_state.typing_status = False
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """获取消息列表
        
        Returns:
            消息列表
        """
        return st.session_state.messages
    
    def get_pending_review(self) -> Optional[Dict[str, Any]]:
        """获取待审核消息
        
        Returns:
            待审核消息或None
        """
        return st.session_state.pending_review
    
    def is_typing(self) -> bool:
        """检查是否正在输入
        
        Returns:
            是否正在输入
        """
        return st.session_state.typing_status
    
    def set_conversation_id(self, conversation_id: str):
        """设置会话ID
        
        Args:
            conversation_id: 会话ID
        """
        st.session_state.conversation_id = conversation_id
    
    def get_conversation_id(self) -> Optional[str]:
        """获取会话ID
        
        Returns:
            会话ID或None
        """
        return st.session_state.conversation_id
    
    def set_api_status(self, connected: bool):
        """设置API连接状态
        
        Args:
            connected: 是否连接成功
        """
        st.session_state.api_connected = connected
    
    def is_api_connected(self) -> bool:
        """检查API是否连接
        
        Returns:
            API是否连接
        """
        return st.session_state.api_connected
    
    def clear_all(self):
        """清空所有数据"""
        st.session_state.messages = []
        st.session_state.pending_review = None
        st.session_state.typing_status = False
        st.session_state.conversation_id = None
    
    def get_message_count(self) -> int:
        """获取消息总数
        
        Returns:
            消息总数
        """
        return len(st.session_state.messages)
    
    def get_pending_count(self) -> int:
        """获取待审核消息数量
        
        Returns:
            待审核消息数量
        """
        return 1 if st.session_state.pending_review else 0