#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试石头剪刀布手势修复
验证Arduino代码修复后的功能
"""

import requests
import time
import json

def test_rps_fix():
    """测试石头剪刀布手势修复"""
    base_url = "http://192.168.1.26:8081"
    
    print("🎯 测试石头剪刀布手势修复")
    print("=" * 50)
    
    # 测试手势列表
    gestures = [
        ("ROCK", "石头 - 握拳"),
        ("PAPER", "布 - 张开"), 
        ("SCISSORS", "剪刀 - 食指中指")
    ]
    
    for gesture_code, description in gestures:
        print(f"\n🎮 测试: {description}")
        print(f"📤 发送命令: {gesture_code}")
        
        try:
            # 发送RPS手势请求
            response = requests.post(
                f"{base_url}/rps",
                json={"gesture": gesture_code},
                timeout=10
            )
            
            print(f"📡 HTTP状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"✅ 服务器响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    
                    if result.get("success"):
                        print(f"✅ {description} 命令发送成功")
                        print("🔍 请观察机械臂是否有动作...")
                        
                        # 等待机械臂动作完成
                        time.sleep(3)
                        
                        # 询问用户是否看到动作
                        print("❓ 你看到机械臂有动作吗？(y/n): ", end="")
                        # 这里我们假设有动作，实际使用时可以手动确认
                        print("假设有动作")
                        
                    else:
                        print(f"❌ {description} 命令发送失败: {result.get('message', '未知错误')}")
                        
                except json.JSONDecodeError:
                    print(f"⚠️ 响应不是JSON格式: {response.text}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"响应内容: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
        
        # 等待一下再测试下一个手势
        time.sleep(2)
    
    print("\n" + "=" * 50)
    print("🎯 石头剪刀布手势测试完成")
    
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
                print("🔍 请观察机械臂是否重置为张开状态...")
                time.sleep(3)
            except json.JSONDecodeError:
                print(f"⚠️ 重置响应不是JSON格式: {response.text}")
        else:
            print(f"❌ 重置HTTP错误: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 重置请求失败: {e}")

if __name__ == "__main__":
    test_rps_fix()
