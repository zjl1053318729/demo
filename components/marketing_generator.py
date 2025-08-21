"""营销文案生成组件"""
import streamlit as st
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from services.marketing_service import MarketingService

def create_marketing_interface(container: st.container, marketing_service: MarketingService):
    """创建营销文案生成界面
    
    Args:
        container: Streamlit容器
        marketing_service: 营销服务实例
    """
    with container:
        # 标题和说明
        # st.markdown("""
        # <div class="marketing-header">
        #     <h3 style="color: #e91e63; margin-bottom: 1rem;">✨ 营销文案生成器</h3>
        #     <p style="color: #666; margin-bottom: 1.5rem;">
        #         输入您的营销文案生成提示词，AI将为您生成专业的营销文案
        #     </p>
        # </div>
        # """, unsafe_allow_html=True)
        
        # 添加预置prompt快捷按钮
        show_marketing_preset_prompts()
        
        # 初始化表单状态
        if 'marketing_form_prompt' not in st.session_state:
            st.session_state.marketing_form_prompt = ""
        
        # 检查预置prompt
        if hasattr(st.session_state, 'marketing_preset_prompt') and st.session_state.marketing_preset_prompt:
            st.session_state.marketing_form_prompt = st.session_state.marketing_preset_prompt
            del st.session_state.marketing_preset_prompt
        
        # 创建输入表单
        with st.form("marketing_form", clear_on_submit=False):
            # 提示词输入
            prompt = st.text_area(
                "📝 营销文案生成提示词",
                value=st.session_state.marketing_form_prompt,
                placeholder="输入营销信号",
                height=150,
                help="包含tags与event",
                key="marketing_prompt_input"
            )
            
            # 生成按钮
            submitted = st.form_submit_button(
                "🚀 生成营销文案",
                type="primary",
                use_container_width=True
            )
        
        # 更新表单状态
        if prompt != st.session_state.marketing_form_prompt:
            st.session_state.marketing_form_prompt = prompt
        
        # 处理表单提交
        if submitted:
            if not prompt.strip():
                st.error("请输入营销文案生成提示词")
                return
            
            # 显示生成中状态
            with st.spinner("🤖 AI正在为您生成营销文案..."):
                # 异步生成文案
                result = asyncio.run(
                    marketing_service.generate_marketing_copy(prompt)
                )
            
            # 显示结果
            display_marketing_result(result)

def display_marketing_result(result: Dict[str, Any]):
    """显示营销文案生成结果
    
    Args:
        result: 生成结果
    """
    if result['success']:
        # 成功生成文案
        st.success("✅ 营销文案生成成功！")
        
        # 显示生成时间
        st.metric("生成时间", datetime.now().strftime("%H:%M:%S"))
        
        # 显示生成的文案
        st.markdown("### 📄 生成的营销文案")
        
        # 使用美观的样式显示文案
        st.markdown(f"""
        <div class="marketing-result">
            <div class="marketing-content">
                {result['content'].replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 操作按钮
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 复制文案按钮
            if st.button("📋 复制文案", use_container_width=True):
                st.write("文案已复制到剪贴板")
                # 注意：实际的复制功能需要JavaScript，这里只是提示
        
        with col2:
            # 下载文案按钮
            st.download_button(
                label="💾 下载文案",
                data=format_marketing_copy_for_download(result),
                file_name=f"营销文案_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col3:
            # 重新生成按钮
            if st.button("🔄 重新生成", use_container_width=True):
                st.rerun()
        
        # 显示使用统计（如果有）
        if 'usage' in result and result['usage']:
            with st.expander("📊 生成统计"):
                usage = result['usage']
                if 'total_tokens' in usage:
                    st.metric("使用Token数", usage['total_tokens'])
                if 'prompt_tokens' in usage:
                    st.metric("输入Token数", usage['prompt_tokens'])
                if 'completion_tokens' in usage:
                    st.metric("输出Token数", usage['completion_tokens'])
    
    else:
        # 生成失败
        st.error(f"❌ 文案生成失败: {result['content']}")
        
        # 显示重试按钮
        if st.button("🔄 重试", type="primary"):
            st.rerun()

def format_marketing_copy_for_download(result: Dict[str, Any]) -> str:
    """格式化营销文案用于下载
    
    Args:
        result: 生成结果
        
    Returns:
        格式化后的文案内容
    """
    content = f"""营销文案生成结果
===================

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

文案内容:
---------
{result['content']}

---
由AI营销文案生成器生成
"""
    return content

def show_marketing_preset_prompts():
    """显示营销文案预置prompt快捷按钮"""
    st.markdown("### 🎯 快速生成")
    
    # 定义预置的营销prompt
    preset_prompts = [
        {
            "label": "中腰部工薪族",
            "prompt": '{"tags":["代发工资","无信用卡","无金融产品","每月转出资金"],"event":"工资到账6000元"}',
            "icon": "💼"
        },
        {
            "label": "泰惠收个体工商户",
            "prompt": '{"tags":["个体工商户","周期性资金支出","周期性资金流入","与多家银行有合作"],"event":"浏览贷款页面超过5分钟"}',
            "icon": "💰"
        }
    ]
    
    # 创建按钮布局
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"{preset_prompts[0]['icon']} {preset_prompts[0]['label']}",
                     use_container_width=True, key="marketing_preset_1"):
            # 将预置prompt设置到session state中
            st.session_state.marketing_preset_prompt = preset_prompts[0]['prompt']
            st.rerun()
    
    with col2:
        if st.button(f"{preset_prompts[1]['icon']} {preset_prompts[1]['label']}",
                     use_container_width=True, key="marketing_preset_2"):
            # 将预置prompt设置到session state中
            st.session_state.marketing_preset_prompt = preset_prompts[1]['prompt']
            st.rerun()
    
    st.markdown("---")

def show_marketing_examples():
    """显示营销文案示例"""
    with st.expander("💡 提示词示例参考"):
        st.markdown("""
        **提示词示例：**
        
        📱 **智能手机广告文案**
        "请为一款配备高性能处理器、专业摄影系统和长续航电池的智能手机生成广告文案。
        目标受众是年轻商务人士，要求突出科技感和专业性，字数控制在200字以内。"
        
        🍕 **餐厅社交媒体文案**
        "为一家正宗意大利披萨餐厅创作社交媒体推广文案，强调手工制作和进口食材，
        目标受众是美食爱好者，风格要温馨亲切，适合朋友圈分享。"
        
        💼 **在线课程邮件营销文案**
        "为数字营销在线课程写一份邮件营销文案，包含SEO、社交媒体营销等模块，
        目标受众是职场新人和创业者，需要包含明确的行动号召和优惠信息。"
        """)

def load_marketing_css():
    """加载营销文案生成器的自定义CSS"""
    st.markdown("""
    <style>
    .marketing-header {
        background: linear-gradient(135deg, #e91e63 0%, #f06292 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .marketing-result {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #e91e63;
    }
    
    .marketing-content {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333;
        white-space: pre-wrap;
    }
    
    .stForm {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def create_marketing_page():
    """创建完整的营销文案生成页面"""
    # 加载自定义样式
    load_marketing_css()
    
    # 页面标题
    st.markdown("""
    <div class="marketing-header">
        <h1>🚀 AI营销文案生成器</h1>
        <p>自动化低成本的生成短信与app推送, 实现初步触达客户</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示使用说明
    # with st.expander("📖 使用说明", expanded=False):
    #     st.markdown("""
    #     **如何使用营销文案生成器：**
        
    #     1. **详细描述**：在文本框中详细描述您的产品或服务
    #     2. **选择类型**：选择适合的文案类型（广告、产品介绍等）
    #     3. **选择受众**：选择您的目标客户群体
    #     4. **生成文案**：点击生成按钮，AI将为您创建专业文案
    #     5. **使用文案**：复制或下载生成的文案用于您的营销活动
        
    #     **提示：**
    #     - 描述越详细，生成的文案越精准
    #     - 可以多次生成，选择最满意的版本
    #     - 生成的文案可以作为基础，再进行个性化调整
    #     """)
    
    # 显示示例
    # show_marketing_examples()