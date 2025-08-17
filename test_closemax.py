#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_closemax():
    """测试机械手全部握拳"""
    
    print("👊 测试机械手全部握拳")
    print("=" * 50)
    
    try:
        # 发送CLOSEMAX命令
        response = requests.post('http://localhost:8081/closemax', 
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
                print("🟢 机械手全部握拳命令发送成功！")
                print("🎯 机械手应该正在移动到完全握拳位置...")
            else:
                print("❌ 机械手全部握拳命令发送失败")
                
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

def test_hand_actions():
    """测试机械手动作序列"""
    
    print("\n🎬 测试机械手动作序列")
    print("=" * 50)
    
    actions = [
        ("全部张开", "/openmax"),
        ("等待3秒", None),
        ("全部握拳", "/closemax"),
        ("等待3秒", None),
        ("重置", "/reset"),
        ("等待2秒", None),
        ("全部握拳", "/closemax")
    ]
    
    for name, endpoint in actions:
        if endpoint is None:
            print(f"⏳ {name}...")
            time.sleep(3 if "3秒" in name else 2)
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

def test_angle_comparison():
    """测试角度对比"""
    
    print("\n📐 角度对比说明")
    print("=" * 50)
    print("🖐️ 机械手角度配置:")
    print("   - 0度: 手指完全张开")
    print("   - 90度: 手指半开")
    print("   - 180度: 手指完全握拳")
    print("")
    print("🎯 动作说明:")
    print("   - OPENMAX: 所有手指移动到0度 (完全张开)")
    print("   - CLOSEMAX: 所有手指移动到180度 (完全握拳)")
    print("   - RESET: 重置到默认张开状态")
    print("")
    print("👊 握拳效果:")
    print("   - 小拇指: 180度 (完全弯曲)")
    print("   - 无名指: 180度 (完全弯曲)")
    print("   - 中指: 180度 (完全弯曲)")
    print("   - 食指: 180度 (完全弯曲)")
    print("   - 大拇指: 180度 (完全弯曲)")
    print("   - 手腕: 90度 (保持中立)")

if __name__ == "__main__":
    test_arduino_connection()
    test_closemax()
    test_hand_actions()
    test_angle_comparison()
    
    print("\n💡 总结")
    print("=" * 50)
    print("✅ 机械手全部握拳功能已添加")
    print("✅ 新命令: CLOSEMAX")
    print("✅ 新端点: /closemax")
    print("🎯 机械手现在可以全部握拳到最大角度(180度)")
    print("👊 所有手指都会移动到完全握拳位置")
    print("🔄 可以配合OPENMAX实现张开-握拳循环")
