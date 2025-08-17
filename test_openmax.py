#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_openmax():
    """测试机械手全部张开到最大"""
    
    print("🖐️ 测试机械手全部张开到最大")
    print("=" * 50)
    
    try:
        # 发送OPENMAX命令
        response = requests.post('http://localhost:8081/openmax', 
                               json={}, 
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            success = result.get('success', False)
            message = result.get('message', '')
            
            print(f"📊 响应状态: {response.status_code}")
            print(f"✅ 成功: {success}")
            print(f"📝 消息: {message}")
            
            if success:
                print("🟢 机械手全部张开到最大命令发送成功！")
                print("🎯 机械手应该正在移动到最大张开位置...")
            else:
                print("❌ 机械手全部张开到最大命令发送失败")
                
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_arduino_connection():
    """测试Arduino连接状态"""
    
    print("\n🔧 测试Arduino连接状态")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:8081/status', timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            connected = result.get('connected', False)
            
            print(f"📊 Arduino连接状态: {'✅ 已连接' if connected else '❌ 未连接'}")
            
            if connected:
                print("🟢 Arduino连接正常，可以发送命令")
            else:
                print("❌ Arduino未连接，请检查硬件连接")
                
        else:
            print(f"❌ 状态检查失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")

def test_sequence():
    """测试一系列命令"""
    
    print("\n🎬 测试命令序列")
    print("=" * 50)
    
    commands = [
        ("重置", "/reset"),
        ("等待2秒", None),
        ("全部张开", "/openmax"),
        ("等待2秒", None),
        ("重置", "/reset")
    ]
    
    for name, endpoint in commands:
        if endpoint is None:
            print(f"⏳ {name}...")
            time.sleep(2)
        else:
            print(f"📤 发送命令: {name}")
            try:
                response = requests.post(f'http://localhost:8081{endpoint}', 
                                       json={}, 
                                       timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    success = result.get('success', False)
                    print(f"   ✅ {name}命令发送{'成功' if success else '失败'}")
                else:
                    print(f"   ❌ {name}命令发送失败: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {name}命令发送异常: {e}")
            
            time.sleep(1)

if __name__ == "__main__":
    test_arduino_connection()
    test_openmax()
    test_sequence()
    
    print("\n💡 总结")
    print("=" * 50)
    print("✅ 机械手全部张开到最大功能已添加")
    print("✅ 新命令: OPENMAX")
    print("✅ 新端点: /openmax")
    print("🎯 机械手现在可以全部张开到最大角度(0度)")
    print("🖐️ 所有手指都会移动到完全张开位置")
