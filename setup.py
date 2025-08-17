#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机械臂项目设置脚本
自动配置和测试系统
"""

import os
import sys
import subprocess
import socket
import requests
import time

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ 需要Python 3.7或更高版本")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """安装Python依赖"""
    print("📦 安装Python依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 连接到外部地址来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def test_network_connectivity():
    """测试网络连接"""
    print("🌐 测试网络连接...")
    try:
        response = requests.get("http://www.google.com", timeout=5)
        print("✅ 网络连接正常")
        return True
    except Exception as e:
        print(f"❌ 网络连接失败: {e}")
        return False

def check_arduino_ports():
    """检查Arduino端口"""
    print("🔌 检查Arduino端口...")
    common_ports = [
        '/dev/ttyUSB0',
        '/dev/ttyUSB1', 
        '/dev/ttyACM0',
        '/dev/ttyACM1',
        'COM1',
        'COM2',
        'COM3',
        'COM4'
    ]
    
    available_ports = []
    for port in common_ports:
        try:
            import serial
            ser = serial.Serial(port, 9600, timeout=1)
            ser.close()
            available_ports.append(port)
            print(f"✅ 发现可用端口: {port}")
        except:
            pass
    
    if available_ports:
        print(f"✅ 找到 {len(available_ports)} 个可用端口")
        return available_ports
    else:
        print("❌ 未找到Arduino端口")
        return []

def update_swift_config(ip_address):
    """更新Swift配置文件中的IP地址"""
    print("📱 更新Swift配置...")
    
    swift_file = "hand/HandController.swift"
    if not os.path.exists(swift_file):
        print(f"❌ 未找到Swift文件: {swift_file}")
        return False
    
    try:
        with open(swift_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换IP地址
        import re
        new_content = re.sub(
            r'private var serverURL = "http://[^"]+"',
            f'private var serverURL = "http://{ip_address}:8081"',
            content
        )
        
        with open(swift_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Swift配置已更新为: {ip_address}")
        return True
    except Exception as e:
        print(f"❌ 更新Swift配置失败: {e}")
        return False

def test_server():
    """测试服务器"""
    print("🧪 测试服务器...")
    try:
        # 启动服务器进程
        process = subprocess.Popen([sys.executable, "gateway_server.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # 等待服务器启动
        time.sleep(3)
        
        # 测试服务器响应
        response = requests.get("http://localhost:8081/status", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器测试成功")
            process.terminate()
            return True
        else:
            print("❌ 服务器响应异常")
            process.terminate()
            return False
    except Exception as e:
        print(f"❌ 服务器测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 机械臂项目设置脚本")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 安装依赖
    if not install_dependencies():
        return
    
    # 测试网络
    if not test_network_connectivity():
        return
    
    # 获取IP地址
    ip_address = get_local_ip()
    print(f"🌐 本机IP地址: {ip_address}")
    
    # 检查Arduino端口
    arduino_ports = check_arduino_ports()
    
    # 更新Swift配置
    update_swift_config(ip_address)
    
    # 测试服务器
    test_server()
    
    print("\n" + "=" * 50)
    print("✅ 设置完成！")
    print(f"📱 手机端连接地址: http://{ip_address}:8081")
    print("🔧 启动服务器: ./start_server.sh")
    print("📱 在Xcode中编译并运行iOS应用")
    
    if arduino_ports:
        print(f"🔌 Arduino端口: {', '.join(arduino_ports)}")
    else:
        print("⚠️  请确保Arduino已连接")

if __name__ == "__main__":
    main()
