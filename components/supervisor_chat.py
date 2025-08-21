"""监督者对话组件"""
import streamlit as st
from typing import List, Dict, Any, Optional, Callable
from components.layout import format_timestamp

def render_supervisor_chat(container: st.container, controls_container: st.container, 
                          messages: List[Dict[str, Any]], pending_review: Optional[Dict[str, Any]],
                          on_approve: Callable[[str], None], on_reject: Callable[[], None]):
    """渲染监督者视角的对话界面
    
    Args:
        container: 对话容器
        controls_container: 控制面板容器
        messages: 消息列表
        pending_review: 待审核消息
        on_approve: 批准回调函数
        on_reject: 拒绝回调函数
    """
    with container:
        # 创建滚动容器
        chat_container = st.container(height=350)
        
        with chat_container:
            # 显示完整对话历史
            render_conversation_history(messages)
            
            # 显示待审核的AI回复
            if pending_review:
                render_pending_review(pending_review)
    
    # 监督者控制面板
    render_supervisor_controls(controls_container, pending_review, on_approve, on_reject)

def render_conversation_history(messages: List[Dict[str, Any]]):
    """渲染对话历史
    
    Args:
        messages: 消息列表
    """
    if not messages:
        st.info("📝 暂无对话记录")
        return
    
    for message in messages:
        sender_icon = "👤" if message['sender'] == 'user' else "🤖"
        sender_name = "用户" if message['sender'] == 'user' else "AI助手"
        
        # 创建消息卡片
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"**{sender_icon}**")
                st.caption(sender_name)
            
            with col2:
                st.markdown(f"**{format_timestamp(message['timestamp'])}**")
                
                # 根据发送者设置不同的样式
                if message['sender'] == 'user':
                    st.info(message['content'])
                else:
                    st.success(message['content'])
        
        st.markdown("---")

def render_pending_review(pending_review: Dict[str, Any]):
    """渲染待审核消息
    
    Args:
        pending_review: 待审核消息数据
    """
    st.markdown("""
    <div class="pending-review fade-in">
        <div class="pending-review-header">🔍 待审核回复</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示原始AI回复
    with st.container():
        st.markdown("""
        <div class="ai-original-response">
            <strong>🤖 AI原始回复:</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(pending_review['original_content'])
        
        # 显示生成时间
        st.caption(f"⏰ 生成时间: {format_timestamp(pending_review['timestamp'])}")

def render_supervisor_controls(controls_container: st.container, 
                             pending_review: Optional[Dict[str, Any]],
                             on_approve: Callable[[str], None], 
                             on_reject: Callable[[], None]):
    """渲染监督者控制面板
    
    Args:
        controls_container: 控制容器
        pending_review: 待审核消息
        on_approve: 批准回调函数
        on_reject: 拒绝回调函数
    """
    with controls_container:
        if pending_review:
            st.markdown("### 📝 审核操作")
            
            # 编辑回复内容
            edited_content = st.text_area(
                "编辑回复内容:",
                value=pending_review['edited_content'],
                height=100,
                key="edit_response",
                help="您可以直接发送AI回复，或编辑后再发送"
            )
            
            # 更新编辑内容到session state
            if edited_content != pending_review['edited_content']:
                st.session_state.pending_review['edited_content'] = edited_content
            
            # 操作按钮
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✅ 直接发送", type="primary", use_container_width=True,
                           help="直接发送AI的原始回复"):
                    on_approve(pending_review['original_content'])
            
            with col2:
                if st.button("📝 编辑后发送", use_container_width=True,
                           help="发送编辑后的回复内容"):
                    on_approve(edited_content)
            
            with col3:
                if st.button("❌ 拒绝回复", use_container_width=True,
                           help="拒绝此回复，重新生成"):
                    on_reject()
            
            # 显示操作提示
            st.markdown("---")
            render_operation_tips()
        
        else:
            render_supervisor_status()

def render_operation_tips():
    """渲染操作提示"""
    with st.expander("💡 操作说明"):
        st.markdown("""
        **审核选项：**
        - **直接发送**: 将AI的原始回复直接发送给用户
        - **编辑后发送**: 修改回复内容后发送给用户
        - **拒绝回复**: 拒绝当前回复，可以重新生成
        
        **编辑建议：**
        - 检查回复的准确性和相关性
        - 确保语言表达清晰友好
        - 避免可能引起误解的内容
        - 保持专业的客服语调
        """)

def render_supervisor_status():
    """渲染监督者状态信息"""
    st.markdown("### 📊 监督状态")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("✅ 等待用户消息")
    
    with col2:
        st.metric("待审核", 0)
    
    # 显示监督者指南
    # with st.expander("📋 监督者指南"):
    #     st.markdown("""
    #     **职责说明：**
    #     - 审核AI生成的所有回复
    #     - 确保回复质量和准确性
    #     - 必要时编辑或拒绝回复
    #     - 维护良好的客服体验
        
    #     **审核标准：**
    #     - 回复内容是否准确
    #     - 语言是否专业友好
    #     - 是否解决用户问题
    #     - 是否符合公司政策
    #     """)

def show_supervisor_welcome():
    """显示监督者欢迎信息"""
    st.markdown("""
    <div class="welcome-message fade-in" style="background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);">
        <div class="welcome-title">👨‍💼 监督者控制台</div>
        <div class="welcome-subtitle">您可以在这里审核和编辑AI回复，确保服务质量</div>
    </div>
    """, unsafe_allow_html=True)

def render_supervisor_metrics(message_count: int, pending_count: int, approval_rate: float = 0.0):
    """渲染监督者指标
    
    Args:
        message_count: 消息总数
        pending_count: 待审核数量
        approval_rate: 批准率
    """
    st.markdown("### 📈 工作统计")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("总消息数", message_count)
    
    with col2:
        st.metric("待审核", pending_count)
    
    with col3:
        st.metric("批准率", f"{approval_rate:.1%}")

def create_supervisor_interface(container: st.container, controls_container: st.container,
                              messages: List[Dict[str, Any]], pending_review: Optional[Dict[str, Any]],
                              message_count: int, on_approve: Callable[[str], None], 
                              on_reject: Callable[[], None]):
    """创建完整的监督者界面
    
    Args:
        container: 主容器
        controls_container: 控制容器
        messages: 消息列表
        pending_review: 待审核消息
        message_count: 消息数量
        on_approve: 批准回调函数
        on_reject: 拒绝回调函数
    """
    # 显示欢迎信息（仅在没有消息时显示）
    if message_count == 0:
        show_supervisor_welcome()
    
    # 渲染监督者界面
    render_supervisor_chat(container, controls_container, messages, pending_review, 
                          on_approve, on_reject)