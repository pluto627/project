#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试HTTP连接脚本
验证iOS应用可以正常连接到服务器
"""

import requests
import json

def test_http_connection():
    """测试HTTP连接"""
    print("🔗 测试HTTP连接...")
    
    # 测试不同的IP地址
    test_urls = [
        "http://localhost:8081/status",
        "http://127.0.0.1:8081/status", 
        "http://192.168.1.26:8081/status",
        "http://198.18.0.1:8081/status"
    ]
    
    for url in test_urls:
        try:
            print(f"测试: {url}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 成功: {url}")
                print(f"   状态: {data.get('status')}")
                print(f"   Arduino: {data.get('arduino_connected')}")
            else:
                print(f"❌ 失败: {url} - HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ 错误: {url} - {e}")
        print()

def test_gesture_commands():
    """测试手势命令"""
    print("🤚 测试手势命令...")
    
    base_url = "http://192.168.1.26:8081"
    
    commands = [
        ("/rps", {"gesture": "ROCK"}),
        ("/rps", {"gesture": "PAPER"}),
        ("/rps", {"gesture": "SCISSORS"})
    ]
    
    for endpoint, data in commands:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.post(url, json=data, timeout=5)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {endpoint}: {result.get('message', 'success')}")
            else:
                print(f"❌ {endpoint}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

if __name__ == "__main__":
    print("🧪 HTTP连接测试")
    print("=" * 50)
    
    test_http_connection()
    test_gesture_commands()
    
    print("=" * 50)
    print("📱 对于iOS应用，请确保:")
    print("   1. 手机和电脑在同一WiFi网络")
    print("   2. 使用正确的IP地址: 192.168.1.26")
    print("   3. Info.plist已配置允许HTTP连接")
    print("   4. 重新编译并运行iOS应用")
