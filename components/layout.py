"""布局组件"""
import streamlit as st
from typing import Tuple

def load_custom_css():
    """加载自定义CSS样式"""
    try:
        with open("static/style.css", "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # 如果CSS文件不存在，使用内联样式
        st.markdown("""
        <style>
        .main { padding-top: 1rem; }
        .user-panel {
            background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .supervisor-panel {
            background: linear-gradient(135deg, #fff3e0 0%, #f1f8e9 100%);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .chat-container {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1rem;
            background: white;
            margin-bottom: 1rem;
        }
        .welcome-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

def create_main_layout() -> Tuple[st.container, st.container, str, st.container]:
    """创建主要布局
    
    Returns:
        用户容器, 监督者容器, 用户输入, 监督者控制容器
    """
    # 加载自定义样式
    load_custom_css()
    
    # 创建标题
    st.markdown("""
    <div class="main-title">
        <h1>🚀 AI营销助手 - 客服对话系统</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 创建双栏布局
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="user-panel">
            <h3 style="color: #1976d2; margin-bottom: 1rem;">👤 用户视角</h3>
        </div>
        """, unsafe_allow_html=True)
        user_container = st.container()
        user_input = st.chat_input("请输入您的问题...", key="user_input")
    
    with col2:
        st.markdown("""
        <div class="supervisor-panel">
            <h3 style="color: #f57c00; margin-bottom: 1rem;">👨‍💼 客户经理视角</h3>
        </div>
        """, unsafe_allow_html=True)
        supervisor_container = st.container()
        supervisor_controls = st.container()
    
    return user_container, supervisor_container, user_input, supervisor_controls

def create_sidebar(state_manager):
    """创建侧边栏
    
    Args:
        state_manager: 状态管理器实例
    """
    with st.sidebar:
        st.markdown("### 📊 系统状态")
        
        # 显示连接状态
        if state_manager.is_api_connected():
            st.success("✅ API连接正常")
        else:
            st.error("❌ API连接异常")
        
        # 显示统计信息
        message_count = state_manager.get_message_count()
        st.metric("消息总数", message_count)
        
        pending_count = state_manager.get_pending_count()
        st.metric("待审核消息", pending_count)
        
        # 显示会话信息
        conversation_id = state_manager.get_conversation_id()
        if conversation_id:
            st.info(f"会话ID: {conversation_id[:8]}...")
        
        st.markdown("---")
        
        # 操作按钮
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ 清空对话", use_container_width=True):
                state_manager.clear_all()
                st.rerun()
        
        with col2:
            if st.button("📥 导出对话", use_container_width=True):
                export_conversation(state_manager)

def export_conversation(state_manager):
    """导出对话记录
    
    Args:
        state_manager: 状态管理器实例
    """
    messages = state_manager.get_messages()
    if not messages:
        st.warning("没有对话记录可导出")
        return
    
    # 生成导出内容
    export_content = "# 对话记录导出\n\n"
    export_content += f"导出时间: {st.session_state.get('export_time', '未知')}\n"
    export_content += f"消息总数: {len(messages)}\n\n"
    
    for i, msg in enumerate(messages, 1):
        sender = "用户" if msg['sender'] == 'user' else "AI助手"
        timestamp = msg['timestamp']
        content = msg['content']
        
        export_content += f"## 消息 {i}\n"
        export_content += f"**发送者**: {sender}\n"
        export_content += f"**时间**: {timestamp}\n"
        export_content += f"**内容**: {content}\n\n"
    
    # 提供下载
    st.download_button(
        label="📄 下载对话记录",
        data=export_content,
        file_name=f"conversation_{st.session_state.get('conversation_id', 'unknown')}.md",
        mime="text/markdown",
        use_container_width=True
    )

def show_typing_indicator():
    """显示输入指示器"""
    with st.container():
        st.markdown(
            """
            <div class="typing-indicator fade-in">
                <div style="margin-right: 10px;">🤖</div>
                <div style="color: #666; font-weight: 500;">AI正在思考中</div>
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def format_timestamp(timestamp_str: str) -> str:
    """格式化时间戳
    
    Args:
        timestamp_str: ISO格式的时间戳字符串
        
    Returns:
        格式化后的时间字符串
    """
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime("%H:%M:%S")
    except:
        return "未知时间"

def create_message_container(height: int = 400) -> st.container:
    """创建消息容器
    
    Args:
        height: 容器高度
        
    Returns:
        消息容器
    """
    return st.container(height=height)