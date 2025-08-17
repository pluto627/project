#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手势识别测试脚本
测试服务器端的手势识别功能
"""

import requests
import json

def test_gesture_recognition():
    """测试手势识别功能"""
    url = "http://192.168.1.26:8081/analyze_hand"
    
    print("🧪 手势识别测试")
    print("=" * 50)
    
    # 模拟石头手势数据（所有手指弯曲）
    rock_data = {
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {
            "x": 0.6, "y": 0.8, "confidence": 0.8
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {
            "x": 0.5, "y": 0.8, "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {
            "x": 0.4, "y": 0.8, "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {
            "x": 0.3, "y": 0.8, "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {
            "x": 0.2, "y": 0.8, "confidence": 0.9
        }
    }
    
    # 模拟剪刀手势数据（食指和中指伸直）
    scissors_data = {
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {
            "x": 0.6, "y": 0.8, "confidence": 0.8
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {
            "x": 0.5, "y": 0.3, "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {
            "x": 0.4, "y": 0.3, "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {
            "x": 0.3, "y": 0.8, "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {
            "x": 0.2, "y": 0.8, "confidence": 0.9
        }
    }
    
    # 模拟布手势数据（所有手指伸直）
    paper_data = {
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {
            "x": 0.6, "y": 0.3, "confidence": 0.8
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {
            "x": 0.5, "y": 0.3, "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {
            "x": 0.4, "y": 0.3, "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {
            "x": 0.3, "y": 0.3, "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {
            "x": 0.2, "y": 0.3, "confidence": 0.9
        }
    }
    
    test_cases = [
        ("石头", rock_data),
        ("剪刀", scissors_data),
        ("布", paper_data)
    ]
    
    for gesture_name, test_data in test_cases:
        print(f"\n🎮 测试手势: {gesture_name}")
        
        try:
            response = requests.post(url, json=test_data, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                print(f"📡 HTTP状态码: {response.status_code}")
                print(f"✅ 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                
                if result.get("success"):
                    detected_gesture = result.get("gesture", "未知")
                    confidence = result.get("confidence", 0.0)
                    print(f"🎯 识别结果: {detected_gesture} (置信度: {confidence:.2f})")
                    
                    if detected_gesture == gesture_name:
                        print("✅ 识别正确!")
                    else:
                        print("❌ 识别错误!")
                else:
                    print("❌ 识别失败")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
        
        print("-" * 30)

def test_real_data():
    """测试真实的手部数据"""
    print("\n🔍 测试真实手部数据")
    print("=" * 50)
    
    # 从服务器日志中提取的真实数据
    real_data = {
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)': {'y': 0.825028657913208, 'confidence': 0.91064453125, 'x': 0.6645155549049377},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKMDIP)': {'x': 0.4016221761703491, 'confidence': 0.96484375, 'y': 0.6710471510887146},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKIPIP)': {'y': 0.7910882830619812, 'confidence': 0.85009765625, 'x': 0.4910745322704315},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKIMCP)': {'confidence': 0.84130859375, 'x': 0.5275192856788635, 'y': 0.7838854789733887},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)': {'x': 0.5552936792373657, 'y': 0.870537519454956, 'confidence': 0.58154296875},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKMMCP)': {'y': 0.7128854393959045, 'confidence': 0.94287109375, 'x': 0.5129085183143616},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKRPIP)': {'confidence': 0.9541015625, 'x': 0.4592811167240143, 'y': 0.5982773303985596},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)': {'y': 0.8348183631896973, 'confidence': 0.5087890625, 'x': 0.5219622254371643},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKIDIP)': {'y': 0.8080971240997314, 'confidence': 0.71435546875, 'x': 0.49323874711990356},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKTMP)': {'y': 0.855145275592804, 'confidence': 0.78466796875, 'x': 0.6170814037322998},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKMPIP)': {'x': 0.4457446038722992, 'confidence': 0.951171875, 'y': 0.6838586330413818},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKPDIP)': {'confidence': 0.96728515625, 'x': 0.4752022624015808, 'y': 0.4699673652648926},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKRMCP)': {'x': 0.5223182439804077, 'confidence': 0.9287109375, 'y': 0.6577161550521851},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)': {'x': 0.4456518888473511, 'confidence': 0.927734375, 'y': 0.4237530827522278},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKTIP)': {'confidence': 0.73583984375, 'y': 0.8509523272514343, 'x': 0.5848215818405151},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKWRI)': {'y': 0.7482308149337769, 'confidence': 0.802734375, 'x': 0.7152201533317566},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)': {'x': 0.37209829688072205, 'y': 0.6570332050323486, 'confidence': 0.95556640625},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)': {'x': 0.38833218812942505, 'y': 0.5434954166412354, 'confidence': 0.96826171875},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKRDIP)': {'x': 0.4190351068973541, 'y': 0.5662558078765869, 'confidence': 0.9521484375},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKPPIP)': {'x': 0.5125377178192139, 'y': 0.5072117447853088, 'confidence': 0.96044921875},
        'VNHumanHandPoseObservationJointName(_rawValue: VNHLKPMCP)': {'y': 0.5733809471130371, 'x': 0.5551382899284363, 'confidence': 0.916015625}
    }
    
    url = "http://192.168.1.26:8081/analyze_hand"
    
    try:
        response = requests.post(url, json=real_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print(f"📡 HTTP状态码: {response.status_code}")
            print(f"✅ 响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result.get("success"):
                detected_gesture = result.get("gesture", "未知")
                confidence = result.get("confidence", 0.0)
                print(f"🎯 识别结果: {detected_gesture} (置信度: {confidence:.2f})")
            else:
                print("❌ 识别失败")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == "__main__":
    test_gesture_recognition()
    test_real_data()
