# 人在回路自动营销系统 - 部署指南

## 🎯 部署概述

本指南将帮助您在不同环境中部署人在回路自动营销系统，包括开发环境、测试环境和生产环境的部署方案。

## 📋 系统要求

### 硬件要求
- **CPU**: 2核心以上
- **内存**: 4GB以上
- **存储**: 10GB可用空间
- **网络**: 稳定的互联网连接

### 软件要求
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.9 或更高版本
- **包管理器**: pip 或 pixi
- **浏览器**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### 外部服务
- **Dify API**: 有效的API密钥和访问权限
- **网络**: 能够访问Dify API服务

## 🚀 快速部署

### 方法一：使用Pixi（推荐）

#### 1. 安装Pixi
```bash
# Windows (PowerShell)
iwr -useb https://pixi.sh/install.ps1 | iex

# macOS/Linux
curl -fsSL https://pixi.sh/install.sh | bash

# 验证安装
pixi --version
```

#### 2. 克隆项目
```bash
git clone <repository-url>
cd ai_customer_service
```

#### 3. 安装依赖
```bash
# 安装所有依赖
pixi install

# 验证安装
pixi list
```

#### 4. 配置环境
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置文件
# Windows: notepad .env
# macOS/Linux: nano .env
```

#### 5. 启动服务
```bash
# 开发环境
pixi run dev

# 生产环境
pixi run start
```

### 方法二：使用传统Python环境

#### 1. 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### 2. 安装依赖
```bash
# 升级pip
pip install --upgrade pip

# 安装依赖
pip install streamlit requests python-dotenv

# 验证安装
pip list
```

#### 3. 配置和启动
```bash
# 配置环境变量
cp .env.example .env
# 编辑.env文件

# 启动应用
streamlit run app.py
```

## ⚙️ 环境配置

### 必需配置项

#### Dify API配置
```bash
# .env文件内容
DIFY_API_KEY=your_dify_api_key_here
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_TIMEOUT=30
```

#### 应用配置
```bash
# 调试模式（开发环境设为true）
APP_DEBUG=false

# 日志级别
LOG_LEVEL=INFO
```

### 可选配置项

#### 高级设置
```bash
# 自定义端口（默认8501）
STREAMLIT_PORT=8501

# 自定义主机（默认localhost）
STREAMLIT_HOST=0.0.0.0

# 最大消息长度
MAX_MESSAGE_LENGTH=1000
```

### 配置验证
```bash
# 使用测试脚本验证配置
python test_imports.py
```

## 🌐 生产环境部署

### Docker部署

#### 1. 创建Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir streamlit requests python-dotenv

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### 2. 构建和运行
```bash
# 构建镜像
docker build -t ai-customer-service .

# 运行容器
docker run -p 8501:8501 --env-file .env ai-customer-service
```

### 云服务部署

#### Heroku部署
```bash
# 安装Heroku CLI
# 创建Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# 部署
heroku create your-app-name
heroku config:set DIFY_API_KEY=your_key
git push heroku main
```

#### AWS EC2部署
```bash
# 连接到EC2实例
ssh -i your-key.pem ubuntu@your-ec2-ip

# 安装依赖
sudo apt update
sudo apt install python3-pip git

# 克隆和部署项目
git clone <repository-url>
cd ai_customer_service
pip3 install -r requirements.txt

# 使用systemd管理服务
sudo nano /etc/systemd/system/ai-customer-service.service
```

#### systemd服务配置
```ini
[Unit]
Description=AI Customer Service System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai_customer_service
Environment=PATH=/home/ubuntu/.local/bin
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🔒 安全配置

### API密钥管理
```bash
# 使用环境变量
export DIFY_API_KEY="your_secure_key"

# 或使用密钥管理服务
# AWS Secrets Manager
# Azure Key Vault
# Google Secret Manager
```

### 网络安全
```bash
# 配置防火墙
sudo ufw allow 8501/tcp
sudo ufw enable

# 使用HTTPS（推荐使用反向代理）
# Nginx配置示例
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 访问控制
```python
# 在app.py中添加认证
import streamlit_authenticator as stauth

# 配置认证
authenticator = stauth.Authenticate(
    credentials,
    'cookie_name',
    'signature_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')
```

## 📊 监控和日志

### 日志配置
```python
# 在config/settings.py中配置
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/ai-customer-service.log'),
        logging.StreamHandler()
    ]
)
```

### 性能监控
```bash
# 使用htop监控系统资源
sudo apt install htop
htop

# 监控应用日志
tail -f app.log

# 监控网络连接
netstat -tulpn | grep 8501
```

### 健康检查
```python
# 添加健康检查端点
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

## 🔧 故障排除

### 常见问题

#### 1. 端口占用
```bash
# 查找占用端口的进程
lsof -i :8501
# 或
netstat -tulpn | grep 8501

# 终止进程
kill -9 <PID>
```

#### 2. 依赖安装失败
```bash
# 清理pip缓存
pip cache purge

# 使用国内镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ streamlit

# 升级pip
python -m pip install --upgrade pip
```

#### 3. API连接失败
```bash
# 测试网络连接
curl -I https://api.dify.ai/v1

# 检查API密钥
echo $DIFY_API_KEY

# 验证配置
python -c "from config.settings import AppConfig; print(AppConfig.load())"
```

#### 4. 内存不足
```bash
# 检查内存使用
free -h

# 增加swap空间
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📈 性能优化

### 应用优化
```python
# 使用缓存减少API调用
@st.cache_data
def cached_api_call(message):
    return api_service.call(message)

# 优化状态管理
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    # 初始化代码
```

### 系统优化
```bash
# 调整系统参数
echo 'net.core.somaxconn = 1024' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_max_syn_backlog = 1024' >> /etc/sysctl.conf
sysctl -p

# 优化文件描述符限制
echo '* soft nofile 65536' >> /etc/security/limits.conf
echo '* hard nofile 65536' >> /etc/security/limits.conf
```

## 🔄 更新和维护

### 应用更新
```bash
# 备份当前版本
cp -r ai_customer_service ai_customer_service_backup

# 拉取最新代码
git pull origin main

# 更新依赖
pixi install
# 或
pip install -r requirements.txt

# 重启服务
sudo systemctl restart ai-customer-service
```

### 数据备份
```bash
# 备份配置文件
cp .env .env.backup

# 备份日志文件
tar -czf logs_backup_$(date +%Y%m%d).tar.gz *.log

# 定期清理日志
find . -name "*.log" -mtime +30 -delete
```

## 📞 技术支持

### 部署支持
- **邮箱**: deployment@example.com
- **文档**: 查看项目README.md
- **社区**: GitHub Issues

### 紧急联系
- **24小时热线**: +86-xxx-xxxx-xxxx
- **紧急邮箱**: emergency@example.com

---

**注意**: 生产环境部署前请进行充分的测试，确保所有功能正常运行。建议先在测试环境中验证部署流程。