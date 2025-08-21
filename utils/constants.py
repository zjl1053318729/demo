"""常量定义"""

# 消息相关常量
MESSAGE_SENDER_USER = "user"
MESSAGE_SENDER_ASSISTANT = "assistant"
MESSAGE_SENDER_SYSTEM = "system"

MESSAGE_STATUS_SENT = "sent"
MESSAGE_STATUS_PENDING = "pending"
MESSAGE_STATUS_FAILED = "failed"

# 界面常量
MAX_MESSAGE_LENGTH = 1000
CHAT_CONTAINER_HEIGHT = 400
DEFAULT_TIMEOUT = 30

# 状态常量
TYPING_STATUS_KEY = "typing_status"
MESSAGES_KEY = "messages"
PENDING_REVIEW_KEY = "pending_review"
CONVERSATION_ID_KEY = "conversation_id"
API_CONNECTED_KEY = "api_connected"

# 错误类型常量
ERROR_TYPE_API = "api_error"
ERROR_TYPE_NETWORK = "network_error"
ERROR_TYPE_TIMEOUT = "timeout_error"
ERROR_TYPE_VALIDATION = "validation_error"
ERROR_TYPE_UNKNOWN = "unknown_error"

# 日志级别
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"

# 界面文本
UI_TEXT = {
    "app_title": "🤖 人在回路自动营销系统",
    "user_perspective": "👤 用户视角",
    "supervisor_perspective": "👨‍💼 客户经理视角",
    "user_input_placeholder": "请输入您的问题...",
    "typing_indicator": "🤖 正在输入...",
    "welcome_user": "👋 欢迎使用人在回路自动营销系统！请在下方输入您的问题。",
    "welcome_supervisor": "👨‍💼 欢迎使用客户经理界面！您可以在这里审核AI回复。",
    "no_messages": "📝 暂无对话记录",
    "pending_review": "🔍 待审核回复",
    "ai_original_reply": "🤖 AI原始回复:",
    "edit_content": "编辑回复内容:",
    "approve_direct": "✅ 直接发送",
    "approve_edited": "📝 编辑后发送",
    "reject_reply": "❌ 拒绝回复",
    "clear_chat": "🗑️ 清空对话",
    "export_chat": "📥 导出对话",
    "api_connected": "✅ API连接正常",
    "api_disconnected": "❌ API连接异常",
    "waiting_user": "✅ 等待用户消息",
    "preparing_reply": "🤖 客户经理正在为您准备回复...",
    "start_conversation": "💬 开始对话吧！",
}

# 帮助文本
HELP_TEXT = {
    "user_tips": """
**如何使用：**
- 在下方输入框中输入您的问题
- 按回车键或点击发送按钮提交
- 等待AI客服回复

**注意事项：**
- 消息长度限制为1000字符
- 请使用文明用语
- 如遇问题请联系客户经理
""",
    "supervisor_operations": """
**审核选项：**
- **直接发送**: 将AI的原始回复直接发送给用户
- **编辑后发送**: 修改回复内容后发送给用户
- **拒绝回复**: 拒绝当前回复，可以重新生成

**编辑建议：**
- 检查回复的准确性和相关性
- 确保语言表达清晰友好
- 避免可能引起误解的内容
- 保持专业的语调
""",
    "supervisor_guide": """
**职责说明：**
- 审核AI生成的所有回复
- 确保回复质量和准确性
- 必要时编辑或拒绝回复
- 维护良好的体验

**审核标准：**
- 回复内容是否准确
- 语言是否专业友好
- 是否解决用户问题
- 是否符合公司政策
""",
}

# API相关常量
API_ENDPOINTS = {
    "chat_messages": "/chat-messages",
    "health": "/health",
}

# 默认配置
DEFAULT_CONFIG = {
    "dify_base_url": "https://api.dify.ai/v1",
    "dify_timeout": 30,
    "app_debug": False,
    "log_level": "INFO",
    "max_message_length": 1000,
}

# 敏感词列表（示例）
SENSITIVE_WORDS = [
    "测试敏感词",
    # 实际使用时可以从配置文件或数据库加载
]

# 文件相关常量
FILE_EXTENSIONS = {
    "log": ".log",
    "markdown": ".md",
    "json": ".json",
    "env": ".env",
}

# 时间格式
TIME_FORMATS = {
    "display": "%H:%M:%S",
    "full": "%Y-%m-%d %H:%M:%S",
    "iso": "%Y-%m-%dT%H:%M:%S",
}

# 颜色主题（用于自定义样式）
COLORS = {
    "primary": "#007bff",
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40",
}

# 图标映射
ICONS = {
    "user": "👤",
    "assistant": "🤖",
    "supervisor": "👨‍💼",
    "system": "⚙️",
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "loading": "⏳",
    "edit": "📝",
    "delete": "🗑️",
    "export": "📥",
    "settings": "⚙️",
}