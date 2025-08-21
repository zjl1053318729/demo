# 人在回路自动营销系统

一个基于Streamlit和Dify API的人工监督AI客服系统demo，实现AI回复的人工审核机制。

## 功能特性

- 🎯 **双视角界面**: 用户视角和监督者视角的并行对话栏
- 🔍 **智能审核流程**: AI回复先经监督者审核再发送给用户
- ⚡ **实时状态同步**: "正在输入"状态和消息状态实时更新
- ✏️ **灵活编辑功能**: 监督者可直接发送或编辑后发送AI回复
- 🔌 **Dify API集成**: 无缝对接Dify平台的AI服务
- 📊 **状态监控**: 实时显示系统状态和统计信息

## 系统架构

```
用户发送消息 → 显示在监督者界面 → 调用Dify API → AI生成回复 
→ 监督者审核 → 批准/编辑/拒绝 → 发送给用户
```

## 快速开始

### 环境要求

- Python 3.9+
- Pixi (推荐) 或 pip
- Dify API访问权限

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd ai_customer_service
```

2. **使用Pixi安装依赖**
```bash
# 初始化pixi环境
pixi install

# 或者添加依赖
pixi add streamlit requests python-dotenv
pixi add --feature dev pytest black flake8 mypy
```

3. **配置环境变量**
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，添加您的Dify API配置
DIFY_API_KEY=your_dify_api_key_here
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_TIMEOUT=30
```

4. **启动应用**
```bash
# 开发环境
pixi run dev

# 生产环境
pixi run start
```

### 传统pip安装

如果不使用pixi，也可以使用传统的pip安装：

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install streamlit requests python-dotenv

# 启动应用
streamlit run app.py
```

## 使用说明

### 用户视角
1. 在左侧"用户视角"栏中输入问题
2. 等待AI客服回复（会显示"正在输入"状态）
3. 收到经过监督者审核的回复

### 监督者视角
1. 在右侧"监督者视角"栏中查看完整对话历史
2. 当AI生成回复后，在"待审核回复"区域查看内容
3. 选择操作：
   - **直接发送**: 发送AI原始回复
   - **编辑后发送**: 修改内容后发送
   - **拒绝回复**: 拒绝当前回复

## 项目结构

```
ai_customer_service/
├── app.py                    # 主应用入口
├── config/                   # 配置模块
│   ├── __init__.py
│   └── settings.py          # 应用配置
├── services/                # 业务服务
│   ├── __init__.py
│   ├── dify_api.py         # Dify API服务
│   └── state_manager.py    # 状态管理服务
├── components/              # UI组件
│   ├── __init__.py
│   ├── layout.py           # 布局组件
│   ├── user_chat.py        # 用户对话组件
│   └── supervisor_chat.py  # 监督者对话组件
├── utils/                   # 工具函数
│   ├── __init__.py
│   ├── helpers.py          # 辅助函数
│   └── constants.py        # 常量定义
├── pixi.toml               # Pixi配置文件
├── .env.example            # 环境变量示例
└── README.md               # 项目说明
```

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DIFY_API_KEY` | Dify API密钥 | 必填 |
| `DIFY_BASE_URL` | Dify API基础URL | `https://api.dify.ai/v1` |
| `DIFY_TIMEOUT` | API请求超时时间(秒) | `30` |
| `APP_DEBUG` | 调试模式 | `false` |
| `LOG_LEVEL` | 日志级别 | `INFO` |

### Pixi任务

| 任务名 | 命令 | 说明 |
|--------|------|------|
| `dev` | `pixi run dev` | 开发环境启动 |
| `start` | `pixi run start` | 生产环境启动 |
| `test` | `pixi run test` | 运行测试 |
| `format` | `pixi run format` | 代码格式化 |
| `lint` | `pixi run lint` | 代码检查 |

## 开发指南

### 添加新功能

1. 在相应模块中添加功能代码
2. 更新相关的UI组件
3. 添加必要的测试
4. 更新文档

### 代码规范

- 使用类型提示
- 遵循PEP 8代码风格
- 编写清晰的文档字符串
- 添加适当的错误处理

### 测试

```bash
# 运行所有测试
pixi run test

# 代码格式化
pixi run format

# 代码检查
pixi run lint
```

## 故障排除

### 常见问题

1. **API连接失败**
   - 检查`DIFY_API_KEY`是否正确
   - 确认网络连接正常
   - 验证API基础URL是否正确

2. **界面显示异常**
   - 清除浏览器缓存
   - 重启Streamlit应用
   - 检查控制台错误信息

3. **消息状态异常**
   - 点击侧边栏"清空对话"重置状态
   - 检查日志文件`app.log`

### 日志查看

应用会在当前目录生成`app.log`日志文件，包含详细的运行信息和错误记录。

## 扩展功能

### 计划中的功能

- [ ] 多监督者支持
- [ ] 权限管理系统
- [ ] 统计分析面板
- [ ] 回复模板管理
- [ ] 多语言支持

### 自定义扩展

系统采用模块化设计，可以轻松扩展：

- 添加新的AI服务提供商
- 自定义审核规则
- 集成外部数据源
- 添加新的UI组件

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交GitHub Issue
- 发送邮件至：[your-email@example.com]

---

**注意**: 这是一个演示项目，生产环境使用前请进行充分的测试和安全评估。