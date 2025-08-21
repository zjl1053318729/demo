# 启动说明

## 🚀 快速启动指南

由于当前环境中没有安装Python或pixi，请按照以下步骤在您的本地环境中运行人在回路自动营销系统：

### 方法一：使用Pixi（推荐）

1. **安装Pixi**
   ```bash
   # Windows (PowerShell)
   iwr -useb https://pixi.sh/install.ps1 | iex
   
   # macOS/Linux
   curl -fsSL https://pixi.sh/install.sh | bash
   ```

2. **安装依赖并启动**
   ```bash
   # 在项目目录中运行
   pixi install
   pixi run dev
   ```

### 方法二：使用传统Python环境

1. **确保Python 3.9+已安装**
   ```bash
   python --version
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install streamlit requests python-dotenv
   ```

4. **配置环境变量**
   ```bash
   # 复制并编辑环境变量文件
   cp .env.example .env
   # 编辑.env文件，设置您的DIFY_API_KEY
   ```

5. **启动应用**
   ```bash
   streamlit run app.py
   ```

## 📋 配置要求

### 必需配置
- `DIFY_API_KEY`: 您的Dify API密钥（必填）
- `DIFY_BASE_URL`: Dify API基础URL（默认：https://api.dify.ai/v1）

### 可选配置
- `DIFY_TIMEOUT`: API请求超时时间（默认：30秒）
- `APP_DEBUG`: 调试模式（默认：false）
- `LOG_LEVEL`: 日志级别（默认：INFO）

## 🎯 功能特性

✅ **已实现的功能：**
- 双视角界面（用户视角 + 监督者视角）
- Dify API集成
- 消息状态管理
- 实时"正在输入"状态
- 监督者审核和编辑功能
- 消息发送确认机制
- 会话历史记录
- 对话导出功能
- 错误处理和日志记录

## 🔧 使用流程

### 用户操作流程：
1. 在左侧"用户视角"输入问题
2. 等待AI回复（显示"正在输入"状态）
3. 收到经过监督者审核的回复

### 监督者操作流程：
1. 在右侧"监督者视角"查看用户消息
2. 查看AI生成的原始回复
3. 选择操作：
   - **直接发送**：发送AI原始回复
   - **编辑后发送**：修改内容后发送
   - **拒绝回复**：拒绝当前回复

## 📊 系统监控

侧边栏显示：
- API连接状态
- 消息总数统计
- 待审核消息数量
- 会话ID信息
- 清空对话和导出功能

## 🐛 故障排除

### 常见问题：

1. **API连接失败**
   - 检查DIFY_API_KEY是否正确设置
   - 确认网络连接正常
   - 验证API基础URL

2. **模块导入错误**
   - 确保所有依赖已正确安装
   - 检查Python版本（需要3.9+）
   - 验证虚拟环境已激活

3. **界面显示异常**
   - 清除浏览器缓存
   - 重启Streamlit应用
   - 检查控制台错误信息

### 日志查看：
应用运行时会生成`app.log`文件，包含详细的运行日志和错误信息。

## 📁 项目结构

```
ai_customer_service/
├── app.py                    # 主应用入口 ⭐
├── config/                   # 配置模块
├── services/                 # 业务服务（API、状态管理）
├── components/               # UI组件（布局、对话界面）
├── utils/                    # 工具函数
├── pixi.toml                # Pixi配置文件
├── .env                     # 环境变量配置
└── README.md                # 详细文档
```

## 🎉 启动成功标志

当应用成功启动后，您将看到：
- 浏览器自动打开 http://localhost:8501
- 左右双栏界面显示正常
- 侧边栏显示系统状态
- API连接状态指示器

## 📞 技术支持

如遇到问题，请：
1. 查看`app.log`日志文件
2. 检查控制台错误信息
3. 参考README.md详细文档
4. 确认所有配置项正确设置

---

**注意**：这是一个演示项目，生产环境使用前请进行充分的测试和安全评估。