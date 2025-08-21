"""人在回路自动营销系统主应用"""
import streamlit as st
import asyncio
import logging
from datetime import datetime

# 导入自定义模块
from config.settings import AppConfig
from services.dify_api import DifyAPIService
from services.marketing_service import MarketingService
from services.state_manager import StateManager
from components.layout import create_main_layout, create_sidebar
from components.user_chat import create_user_interface, validate_user_input
from components.supervisor_chat import create_supervisor_interface
from components.marketing_generator import create_marketing_interface, create_marketing_page
from utils.helpers import setup_logging, handle_error, log_user_action, generate_session_id
from utils.constants import UI_TEXT

class AICustomerServiceApp:
    """人在回路自动营销系统主应用类"""
    
    def __init__(self):
        self.config = None
        self.dify_service = None
        self.marketing_service = None
        self.state_manager = None
        self.logger = None
        
    def initialize(self):
        """初始化应用"""
        try:
            # 加载配置
            self.config = AppConfig.load()
            
            # 设置日志
            setup_logging(self.config.log_level)
            self.logger = logging.getLogger(__name__)
            
            # 初始化服务
            self.dify_service = DifyAPIService(self.config.dify)
            self.marketing_service = MarketingService(self.config.dify)
            self.state_manager = StateManager()
            
            # 设置页面配置
            st.set_page_config(
                page_title=self.config.title,
                page_icon=self.config.page_icon,
                layout=self.config.layout,
                initial_sidebar_state="expanded"
            )
            
            # 初始化会话ID
            if 'session_id' not in st.session_state:
                st.session_state.session_id = generate_session_id()
            
            # 测试API连接
            self._test_api_connection()
            
            self.logger.info("应用初始化成功")
            
        except Exception as e:
            st.error(f"应用初始化失败: {str(e)}")
            self.logger.error(f"应用初始化失败: {e}")
            st.stop()
    
    def _test_api_connection(self):
        """测试API连接"""
        try:
            connected = self.dify_service.test_connection()
            self.state_manager.set_api_status(connected)
            if connected:
                self.logger.info("API连接测试成功")
            else:
                self.logger.warning("API连接测试失败")
        except Exception as e:
            self.logger.error(f"API连接测试异常: {e}")
            self.state_manager.set_api_status(False)
    
    @handle_error
    async def process_user_message(self, user_input: str):
        """处理用户消息
        
        Args:
            user_input: 用户输入内容
        """
        # 验证输入
        is_valid, error_msg = validate_user_input(user_input, self.config.max_message_length)
        if not is_valid:
            st.error(error_msg)
            return
        
        # 记录用户操作
        log_user_action("send_message", {"content_length": len(user_input)})
        
        # 添加用户消息
        user_message = self.state_manager.add_user_message(user_input)
        self.logger.info(f"用户消息已添加: {user_message.id}")
        
        # 设置输入状态
        self.state_manager.set_typing_status(True)
        
        # 调用AI服务
        conversation_id = self.state_manager.get_conversation_id()
        ai_response = await self.dify_service.chat_completion(user_input, conversation_id)
        
        if ai_response['success']:
            # 保存会话ID
            if ai_response.get('conversation_id'):
                self.state_manager.set_conversation_id(ai_response['conversation_id'])
            
            # 设置待审核消息
            self.state_manager.set_pending_review(ai_response['content'], user_message.id)
            self.logger.info(f"AI回复已生成，等待审核")
            
        else:
            # 处理错误
            self.state_manager.set_typing_status(False)
            st.error(f"AI服务调用失败: {ai_response.get('content', '未知错误')}")
            self.logger.error(f"AI服务调用失败: {ai_response}")
        
        # 刷新界面
        st.rerun()
    
    def approve_message(self, final_content: str):
        """批准消息
        
        Args:
            final_content: 最终内容
        """
        try:
            # 记录监督者操作
            log_user_action("approve_message", {"content_length": len(final_content)})
            
            # 批准消息
            message = self.state_manager.approve_message(final_content)
            if message:
                self.logger.info(f"消息已批准发送: {message.id}")
                st.success("消息已发送给用户")
            
            # 刷新界面
            st.rerun()
            
        except Exception as e:
            st.error(f"批准消息失败: {str(e)}")
            self.logger.error(f"批准消息失败: {e}")
    
    def reject_message(self):
        """拒绝消息"""
        try:
            # 记录监督者操作
            log_user_action("reject_message")
            
            # 拒绝消息
            self.state_manager.reject_message()
            self.logger.info("消息已被拒绝")
            st.warning("消息已拒绝，请重新生成回复")
            
            # 刷新界面
            st.rerun()
            
        except Exception as e:
            st.error(f"拒绝消息失败: {str(e)}")
            self.logger.error(f"拒绝消息失败: {e}")
    
    def render_interface(self):
        """渲染界面"""
        # 创建页面导航
        page = self.create_navigation()
        
        if page == "AI客服对话":
            self.render_chat_interface()
        elif page == "营销文案生成":
            self.render_marketing_interface()
    
    def create_navigation(self) -> str:
        """创建页面导航
        
        Returns:
            选中的页面名称
        """
        st.sidebar.markdown("### 🧭 功能导航")
        page = st.sidebar.radio(
            "选择功能",
            ["AI客服对话", "营销文案生成"],
            index=0
        )
        st.sidebar.markdown("---")
        return page
    
    def render_chat_interface(self):
        """渲染AI客服对话界面"""
        # 创建主布局
        user_container, supervisor_container, user_input, supervisor_controls = create_main_layout()
        
        # 创建侧边栏
        create_sidebar(self.state_manager)
        
        # 获取当前状态
        messages = self.state_manager.get_messages()
        pending_review = self.state_manager.get_pending_review()
        is_typing = self.state_manager.is_typing()
        message_count = self.state_manager.get_message_count()
        
        # 渲染用户界面
        create_user_interface(
            user_container,
            messages,
            is_typing,
            message_count
        )
        
        # 渲染监督者界面
        create_supervisor_interface(
            supervisor_container,
            supervisor_controls,
            messages,
            pending_review,
            message_count,
            self.approve_message,
            self.reject_message
        )
        
        # 处理用户输入
        if user_input:
            # 使用asyncio运行异步函数
            asyncio.run(self.process_user_message(user_input))
        
        # 处理预置prompt
        if hasattr(st.session_state, 'preset_prompt') and st.session_state.preset_prompt:
            preset_prompt = st.session_state.preset_prompt
            st.session_state.preset_prompt = None  # 清除预置prompt
            # 使用asyncio运行异步函数
            asyncio.run(self.process_user_message(preset_prompt))
    
    def render_marketing_interface(self):
        """渲染营销文案生成界面"""
        # 创建营销文案生成页面
        create_marketing_page()
        
        # 创建营销文案生成界面
        marketing_container = st.container()
        create_marketing_interface(marketing_container, self.marketing_service)
    
    def run(self):
        """运行应用"""
        self.initialize()
        self.render_interface()

def main():
    """主函数"""
    app = AICustomerServiceApp()
    app.run()

if __name__ == "__main__":
    main()