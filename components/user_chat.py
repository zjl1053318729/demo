"""用户对话组件"""
import streamlit as st
from typing import List, Dict, Any
from components.layout import format_timestamp, show_typing_indicator

def render_user_chat(container: st.container, messages: List[Dict[str, Any]], is_typing: bool = False):
    """渲染用户视角的对话界面
    
    Args:
        container: Streamlit容器
        messages: 消息列表
        is_typing: 是否正在输入
    """
    with container:
        # 创建滚动容器
        chat_container = st.container(height=400)
        
        with chat_container:
            # 显示对话历史
            for message in messages:
                if message['sender'] == 'user':
                    render_user_message(message)
                elif message['sender'] == 'assistant' and message['status'] == 'sent':
                    render_assistant_message(message)
            
            # 显示"正在输入"状态
            if is_typing:
                show_typing_indicator()

def render_user_message(message: Dict[str, Any]):
    """渲染用户消息
    
    Args:
        message: 消息数据
    """
    with st.chat_message("user", avatar="👤"):
        st.write(message['content'])
        st.caption(f"发送时间: {format_timestamp(message['timestamp'])}")

def render_assistant_message(message: Dict[str, Any]):
    """渲染AI助手消息
    
    Args:
        message: 消息数据
    """
    with st.chat_message("assistant", avatar="🤖"):
        st.write(message['content'])
        st.caption(f"回复时间: {format_timestamp(message['timestamp'])}")

def show_user_welcome():
    """显示用户欢迎信息"""
    st.markdown("""
    <div class="welcome-message fade-in">
        <div class="welcome-title">👋 欢迎使用AI客服系统</div>
        <div class="welcome-subtitle">我是您的智能客服助手，有什么可以帮助您的吗？</div>
    </div>
    """, unsafe_allow_html=True)

def show_user_status(message_count: int, is_typing: bool):
    """显示用户状态信息
    
    Args:
        message_count: 消息数量
        is_typing: 是否正在输入
    """
    status_container = st.container()
    
    with status_container:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if is_typing:
                st.info("🤖 客服正在为您准备回复...")
            elif message_count == 0:
                # st.info("💬 开始对话吧！")
                pass
            else:
                st.success(f"✅ 已发送 {message_count} 条消息")
        
        with col2:
            if message_count > 0:
                st.metric("消息", message_count)

def validate_user_input(user_input: str, max_length: int = 1000) -> tuple:
    """验证用户输入
    
    Args:
        user_input: 用户输入内容
        max_length: 最大长度限制
        
    Returns:
        (是否有效, 错误信息)
    """
    if not user_input or not user_input.strip():
        return False, "请输入有效的消息内容"
    
    if len(user_input) > max_length:
        return False, f"消息长度不能超过 {max_length} 个字符"
    
    # 检查是否包含敏感内容（简单示例）
    sensitive_words = ["测试敏感词"]  # 实际使用时可以从配置文件加载
    for word in sensitive_words:
        if word in user_input:
            return False, f"消息包含不当内容: {word}"
    
    return True, ""

def show_input_help():
    """显示输入帮助信息"""
    with st.expander("💡 使用提示", expanded=False):
        st.markdown("""
        <div class="help-section">
            <div class="help-title">📝 如何使用</div>
            <div class="help-content">
                • 在下方输入框中输入您的问题<br>
                • 按回车键或点击发送按钮提交<br>
                • 等待AI客服回复
            </div>
            
            <div class="help-title" style="margin-top: 1rem;">⚠️ 注意事项</div>
            <div class="help-content">
                • 消息长度限制为1000字符<br>
                • 请使用文明用语<br>
                • 如遇问题请联系人工客服
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_preset_prompts():
    """显示预置prompt快捷按钮"""
    st.markdown("### 🚀 快速问题")
    
    # 定义预置的prompt
    preset_prompts = [
        {
            "label": "产品咨询",
            "prompt": "你好，我想了解一下你们的产品特点和优势，能详细介绍一下吗？",
            "icon": "🛍️"
        },
        {
            "label": "技术支持",
            "prompt": "我在使用产品时遇到了一些技术问题，需要帮助解决。",
            "icon": "🔧"
        }
    ]
    
    # 创建按钮布局
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"{preset_prompts[0]['icon']} {preset_prompts[0]['label']}",
                     use_container_width=True, key="preset_1"):
            # 将预置prompt设置到session state中，供主应用使用
            st.session_state.preset_prompt = preset_prompts[0]['prompt']
            st.rerun()
    
    with col2:
        if st.button(f"{preset_prompts[1]['icon']} {preset_prompts[1]['label']}",
                     use_container_width=True, key="preset_2"):
            # 将预置prompt设置到session state中，供主应用使用
            st.session_state.preset_prompt = preset_prompts[1]['prompt']
            st.rerun()
    
    st.markdown("---")

def create_user_interface(container: st.container, messages: List[Dict[str, Any]],
                         is_typing: bool, message_count: int):
    """创建完整的用户界面
    
    Args:
        container: 主容器
        messages: 消息列表
        is_typing: 是否正在输入
        message_count: 消息数量
    """
    with container:
        # 显示欢迎信息（仅在没有消息时显示）
        # if message_count == 0:
        #     show_user_welcome()
        #     show_input_help()
        
        # 添加预置prompt快捷按钮
        show_preset_prompts()
        
        # 显示状态信息
        show_user_status(message_count, is_typing)
        
        # 渲染对话
        render_user_chat(st.container(), messages, is_typing)