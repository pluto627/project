#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试手动按钮功能
模拟iOS应用发送的手动测试请求
"""

import requests
import json
import time

def test_manual_buttons():
    """测试手动按钮功能"""
    base_url = "http://192.168.1.26:8081"
    
    print("🧪 测试手动按钮功能")
    print("=" * 50)
    
    # 测试手势列表
    gestures = [
        ("石头", "ROCK"),
        ("剪刀", "SCISSORS"), 
        ("布", "PAPER")
    ]
    
    for gesture_name, gesture_code in gestures:
        print(f"\n🎮 测试手势: {gesture_name} ({gesture_code})")
        
        # 发送RPS手势请求
        try:
            response = requests.post(
                f"{base_url}/rps",
                json={"gesture": gesture_code},
                timeout=10
            )
            
            print(f"📡 HTTP状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"✅ 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    
                    if result.get("success"):
                        print(f"✅ {gesture_name} 手势发送成功")
                    else:
                        print(f"❌ {gesture_name} 手势发送失败: {result.get('message', '未知错误')}")
                        
                except json.JSONDecodeError:
                    print(f"⚠️ 响应不是JSON格式: {response.text}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"响应内容: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
        
        # 等待一下再测试下一个手势
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎯 测试完成")
    
    # 测试重置功能
    print("\n🔄 测试重置功能")
    try:
        response = requests.post(
            f"{base_url}/reset",
            json={},
            timeout=10
        )
        
        print(f"📡 重置HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ 重置响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            except json.JSONDecodeError:
                print(f"⚠️ 重置响应不是JSON格式: {response.text}")
        else:
            print(f"❌ 重置HTTP错误: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 重置请求失败: {e}")

if __name__ == "__main__":
    test_manual_buttons()
