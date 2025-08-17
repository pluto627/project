#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机械臂系统测试脚本
测试各个组件是否正常工作
"""

import requests
import json
import time
import sys
import os

# 添加虚拟环境路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'venv', 'lib', 'python3.13', 'site-packages'))

def test_server_connection():
    """测试服务器连接"""
    print("🔗 测试服务器连接...")
    try:
        response = requests.get("http://localhost:8081/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 服务器连接成功")
            print(f"   状态: {data.get('status', 'unknown')}")
            print(f"   Arduino连接: {data.get('arduino_connected', False)}")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return False

def test_gesture_recognition():
    """测试手势识别"""
    print("🤚 测试手势识别...")
    
    # 模拟手部关键点数据
    test_hand_data = {
        "thumbTip": {"x": 0.5, "y": 0.3, "confidence": 0.8},
        "indexTip": {"x": 0.6, "y": 0.2, "confidence": 0.9},
        "middleTip": {"x": 0.7, "y": 0.2, "confidence": 0.9},
        "ringTip": {"x": 0.8, "y": 0.4, "confidence": 0.7},
        "pinkyTip": {"x": 0.9, "y": 0.5, "confidence": 0.6}
    }
    
    try:
        response = requests.post(
            "http://localhost:8081/analyze_hand",
            json=test_hand_data,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 手势识别成功")
            print(f"   识别手势: {data.get('gesture', 'unknown')}")
            print(f"   置信度: {data.get('confidence', 0.0):.2f}")
            return True
        else:
            print(f"❌ 手势识别失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 手势识别测试失败: {e}")
        return False

def test_arduino_commands():
    """测试Arduino命令"""
    print("🤖 测试Arduino命令...")
    
    commands = [
        ("/rps", {"gesture": "ROCK"}),
        ("/rps", {"gesture": "PAPER"}),
        ("/rps", {"gesture": "SCISSORS"}),
        ("/number", {"number": "5"}),
        ("/reset", {})
    ]
    
    success_count = 0
    for endpoint, data in commands:
        try:
            response = requests.post(
                f"http://localhost:8081{endpoint}",
                json=data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success', False):
                    success_count += 1
                    print(f"   ✅ {endpoint}: {data}")
                else:
                    print(f"   ⚠️  {endpoint}: {result.get('message', 'unknown error')}")
            else:
                print(f"   ❌ {endpoint}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {endpoint}: {e}")
    
    print(f"✅ Arduino命令测试完成: {success_count}/{len(commands)} 成功")
    return success_count > 0

def test_swift_config():
    """测试Swift配置"""
    print("📱 测试Swift配置...")
    
    swift_file = "hand/HandController.swift"
    if not os.path.exists(swift_file):
        print("❌ Swift配置文件不存在")
        return False
    
    try:
        with open(swift_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'serverURL' in content:
            print("✅ Swift配置文件存在")
            return True
        else:
            print("❌ Swift配置文件中缺少serverURL")
            return False
    except Exception as e:
        print(f"❌ 读取Swift配置失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 机械臂系统测试")
    print("=" * 50)
    
    tests = [
        ("服务器连接", test_server_connection),
        ("手势识别", test_gesture_recognition),
        ("Arduino命令", test_arduino_commands),
        ("Swift配置", test_swift_config)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！系统准备就绪。")
        print("\n📋 下一步:")
        print("   1. 连接Arduino到电脑")
        print("   2. 上传Arduino代码")
        print("   3. 在Xcode中编译iOS应用")
        print("   4. 在手机上运行应用")
        print("   5. 开始石头剪刀布游戏！")
    else:
        print("⚠️  部分测试失败，请检查配置。")
        print("\n🔧 故障排除:")
        print("   1. 确保网关服务器正在运行")
        print("   2. 检查网络连接")
        print("   3. 验证Arduino连接")
        print("   4. 检查Swift配置")

if __name__ == "__main__":
    main()
