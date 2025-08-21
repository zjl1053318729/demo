"""测试导入和基本语法"""
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有模块的导入"""
    try:
        # 测试配置模块
        from config.settings import AppConfig, DifyConfig
        print("✅ 配置模块导入成功")
        
        # 测试服务模块
        from services.dify_api import DifyAPIService
        from services.state_manager import StateManager, Message, PendingReview
        print("✅ 服务模块导入成功")
        
        # 测试组件模块
        from components.layout import create_main_layout, create_sidebar
        from components.user_chat import render_user_chat, validate_user_input
        from components.supervisor_chat import render_supervisor_chat
        print("✅ 组件模块导入成功")
        
        # 测试工具模块
        from utils.helpers import setup_logging, handle_error
        from utils.constants import UI_TEXT, MESSAGE_SENDER_USER
        print("✅ 工具模块导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except SyntaxError as e:
        print(f"❌ 语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    try:
        # 测试配置类
        config = DifyConfig(
            api_key="test_key",
            base_url="https://api.dify.ai/v1",
            timeout=30
        )
        config.validate()
        print("✅ 配置类测试成功")
        
        # 测试消息类
        from datetime import datetime
        message = Message(
            id="test_id",
            content="测试消息",
            sender="user",
            timestamp=datetime.now(),
            status="sent"
        )
        message_dict = message.to_dict()
        print("✅ 消息类测试成功")
        
        # 测试常量
        from utils.constants import UI_TEXT
        assert UI_TEXT["app_title"] == "🤖 人在回路自动营销系统"
        print("✅ 常量测试成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试人在回路自动营销系统...")
    print("=" * 50)
    
    # 测试导入
    import_success = test_imports()
    
    if import_success:
        # 测试基本功能
        func_success = test_basic_functionality()
        
        if func_success:
            print("=" * 50)
            print("🎉 所有测试通过！系统准备就绪。")
            print("\n📋 使用说明:")
            print("1. 确保已安装Python 3.9+")
            print("2. 安装依赖: pip install streamlit requests python-dotenv")
            print("3. 配置.env文件中的DIFY_API_KEY")
            print("4. 运行: streamlit run app.py")
        else:
            print("=" * 50)
            print("❌ 功能测试失败")
    else:
        print("=" * 50)
        print("❌ 导入测试失败")