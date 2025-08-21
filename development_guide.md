# 开发指南

## 项目开发流程

### 阶段一：项目初始化 (预计时间: 30分钟)

#### 1.1 环境准备
```bash
# 初始化pixi项目
pixi init ai_customer_service
cd ai_customer_service

# 或者在现有目录中初始化
pixi init .
```

#### 1.2 依赖安装
```bash
# 添加核心依赖
pixi add streamlit requests python-dotenv

# 添加开发依赖
pixi add --feature dev pytest black flake8 mypy

# 安装所有依赖
pixi install
```

#### 1.3 项目结构创建
```
ai_customer_service/
├── app.py                    # 主应用入口
├── components/               # UI组件
│   ├── __init__.py
│   ├── user_chat.py         # 用户对话组件
│   ├── supervisor_chat.py   # 监督者对话组件
│   └── layout.py            # 布局组件
├── services/                # 业务服务
│   ├── __init__.py
│   ├── dify_api.py         # Dify API服务
│   └── state_manager.py    # 状态管理服务
├── utils/                   # 工具函数
│   ├── __init__.py
│   ├── helpers.py          # 辅助函数
│   └── constants.py        # 常量定义
├── config/                  # 配置文件
│   ├── __init__.py
│   └── settings.py         # 应用配置
├── tests/                   # 测试文件
│   ├── __init__.py
│   ├── test_api.py
│   └── test_components.py
├── static/                  # 静态资源
│   ├── css/
│   └── images/
├── requirements.txt         # 依赖列表
├── .env.example            # 环境变量示例
├── .gitignore              # Git忽略文件
└── README.md               # 项目说明
```

### 阶段二：核心功能开发 (预计时间: 4-6小时)

#### 2.1 配置系统开发 (30分钟)
- 创建配置管理类
- 环境变量处理
- 配置验证机制

#### 2.2 API服务开发 (1小时)
- Dify API集成
- 错误处理机制
- 异步调用实现

#### 2.3 状态管理开发 (1小时)
- 消息状态管理
- 会话状态维护
- 数据持久化

#### 2.4 UI组件开发 (2-3小时)
- 双栏布局实现
- 用户对话界面
- 监督者控制面板
- 消息渲染组件

#### 2.5 主应用集成 (1小时)
- 组件整合
- 事件处理
- 状态同步

### 阶段三：功能完善 (预计时间: 2-3小时)

#### 3.1 用户体验优化
- 加载状态显示
- 错误提示优化
- 界面美化

#### 3.2 功能增强
- 消息历史记录
- 会话管理
- 快捷操作

#### 3.3 测试和调试
- 功能测试
- 边界情况处理
- 性能优化

## 详细实现步骤

### 步骤1: 创建基础配置

```python
# config/settings.py
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DifyConfig:
    api_key: str
    base_url: str
    timeout: int = 30
    
    @classmethod
    def from_env(cls):
        return cls(
            api_key=os.getenv('DIFY_API_KEY', ''),
            base_url=os.getenv('DIFY_BASE_URL', 'https://api.dify.ai/v1'),
            timeout=int(os.getenv('DIFY_TIMEOUT', '30'))
        )

@dataclass
class AppConfig:
    title: str = "人在回路自动营销系统"
    page_icon: str = "🤖"
    layout: str = "wide"
    max_message_length: int = 1000
    
    dify: Optional[DifyConfig] = None
    
    @classmethod
    def load(cls):
        config = cls()
        config.dify = DifyConfig.from_env()
        return config
```

### 步骤2: 实现API服务

```python
# services/dify_api.py
import requests
import asyncio
import logging
from typing import Dict, Any, Optional
from config.settings import DifyConfig

class DifyAPIService:
    def __init__(self, config: DifyConfig):
        self.config = config
        self.headers = {
            'Authorization': f'Bearer {config.api_key}',
            'Content-Type': 'application/json'
        }
        self.logger = logging.getLogger(__name__)
    
    async def chat_completion(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """异步调用Dify聊天API"""
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
            
            return {
                'success': True,
                'content': data.get('answer', ''),
                'conversation_id': data.get('conversation_id'),
                'message_id': data.get('message_id')
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API调用失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': '抱歉，AI服务暂时不可用，请稍后再试。'
            }
        except Exception as e:
            self.logger.error(f"未知错误: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': '系统出现错误，请联系管理员。'
            }
```

### 步骤3: 实现状态管理

```python
# services/state_manager.py
import streamlit as st
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class Message:
    id: str
    content: str
    sender: str  # 'user', 'assistant', 'system'
    timestamp: datetime
    status: str  # 'sent', 'pending', 'failed'
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class PendingReview:
    id: str
    original_content: str
    edited_content: str
    timestamp: datetime
    user_message_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class StateManager:
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
    
    def add_user_message(self, content: str) -> Message:
        """添加用户消息"""
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
        """设置输入状态"""
        st.session_state.typing_status = status
    
    def set_pending_review(self, content: str, user_message_id: str) -> PendingReview:
        """设置待审核消息"""
        pending = PendingReview(
            id=str(uuid.uuid4()),
            original_content=content,
            edited_content=content,
            timestamp=datetime.now(),
            user_message_id=user_message_id
        )
        st.session_state.pending_review = pending.to_dict()
        return pending
    
    def approve_message(self, final_content: str) -> Message:
        """批准并发送消息"""
        if not st.session_state.pending_review:
            return None
        
        message = Message(
            id=st.session_state.pending_review['id'],
            content=final_content,
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
        """获取消息列表"""
        return st.session_state.messages
    
    def get_pending_review(self) -> Optional[Dict[str, Any]]:
        """获取待审核消息"""
        return st.session_state.pending_review
    
    def is_typing(self) -> bool:
        """检查是否正在输入"""
        return st.session_state.typing_status
```

### 步骤4: 创建UI组件

```python
# components/layout.py
import streamlit as st
from typing import Tuple

def create_main_layout() -> Tuple[st.container, st.container, str, st.container]:
    """创建主要布局"""
    st.title("🤖 人在回路自动营销系统")
    st.markdown("---")
    
    # 创建双栏布局
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown("### 👤 用户视角")
        user_container = st.container()
        user_input = st.chat_input("请输入您的问题...", key="user_input")
    
    with col2:
        st.markdown("### 👨‍💼 监督者视角")
        supervisor_container = st.container()
        supervisor_controls = st.container()
    
    return user_container, supervisor_container, user_input, supervisor_controls

def create_sidebar():
    """创建侧边栏"""
    with st.sidebar:
        st.markdown("### 📊 系统状态")
        
        # 显示连接状态
        if st.session_state.get('api_connected', False):
            st.success("✅ API连接正常")
        else:
            st.error("❌ API连接异常")
        
        # 显示统计信息
        message_count = len(st.session_state.get('messages', []))
        st.metric("消息总数", message_count)
        
        pending_count = 1 if st.session_state.get('pending_review') else 0
        st.metric("待审核消息", pending_count)
        
        st.markdown("---")
        
        # 操作按钮
        if st.button("🗑️ 清空对话"):
            st.session_state.messages = []
            st.session_state.pending_review = None
            st.session_state.typing_status = False
            st.rerun()
        
        if st.button("📥 导出对话"):
            # TODO: 实现对话导出功能
            st.info("导出功能开发中...")
```

## 开发最佳实践

### 1. 代码规范
- 使用类型提示 (Type Hints)
- 遵循PEP 8代码风格
- 编写清晰的文档字符串
- 使用有意义的变量和函数名

### 2. 错误处理
- 实现全面的异常捕获
- 提供用户友好的错误信息
- 记录详细的错误日志
- 实现优雅的降级机制

### 3. 性能优化
- 使用异步处理提高响应速度
- 实现适当的缓存机制
- 优化大量数据的渲染
- 减少不必要的API调用

### 4. 安全考虑
- 验证和清理用户输入
- 安全存储API密钥
- 实现访问控制
- 防止XSS和注入攻击

### 5. 测试策略
- 编写单元测试
- 进行集成测试
- 模拟API响应进行测试
- 测试边界情况和错误场景

## 部署准备

### 1. 环境变量配置
```bash
# .env文件示例
DIFY_API_KEY=your_dify_api_key_here
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_TIMEOUT=30

# 应用配置
APP_DEBUG=false
LOG_LEVEL=INFO
```

### 2. Pixi配置文件
```toml
# pixi.toml
[project]
name = "ai_customer_service"
version = "0.1.0"
description = "人在回路自动营销系统"
authors = ["Your Name <your.email@example.com>"]
channels = ["conda-forge", "pola-rs"]
platforms = ["win-64", "linux-64", "osx-64", "osx-arm64"]

[dependencies]
python = ">=3.9,<3.12"
streamlit = ">=1.28.0"
requests = ">=2.31.0"
python-dotenv = ">=1.0.0"

[feature.dev.dependencies]
pytest = "*"
black = "*"
flake8 = "*"
mypy = "*"

[tasks]
start = "streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
dev = "streamlit run app.py --server.port 8501"
test = "pytest tests/"
format = "black ."
lint = "flake8 ."
typecheck = "mypy ."
```

### 3. 启动脚本
```bash
# 开发环境启动
pixi run dev

# 生产环境启动
pixi run start

# 运行测试
pixi run test

# 代码格式化
pixi run format

# 代码检查
pixi run lint
```

这个开发指南提供了详细的实施步骤和最佳实践，确保项目能够高质量地完成开发。