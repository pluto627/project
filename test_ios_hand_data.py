#!/usr/bin/env python3
"""
测试iOS应用发送的手部数据格式
"""

import requests
import json
import time

def test_ios_hand_data():
    """测试iOS应用发送的手部数据格式"""
    
    # iOS Vision框架发送的手部数据格式
    ios_hand_data = {
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {
            "x": 0.5,
            "y": 0.3,
            "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {
            "x": 0.4,
            "y": 0.2,
            "confidence": 0.8
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {
            "x": 0.3,
            "y": 0.4,
            "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {
            "x": 0.2,
            "y": 0.5,
            "confidence": 0.9
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {
            "x": 0.1,
            "y": 0.6,
            "confidence": 0.8
        },
        "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {
            "x": 0.0,
            "y": 0.7,
            "confidence": 0.8
        }
    }
    
    print("🧪 测试iOS手部数据格式")
    print("=" * 50)
    
    try:
        response = requests.post(
            "http://192.168.1.26:8081/analyze_hand",
            json=ios_hand_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"📡 HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get("success"):
                gesture = result.get("gesture", "未知")
                confidence = result.get("confidence", 0.0)
                print(f"🎯 识别结果: {gesture} (置信度: {confidence:.2f})")
            else:
                print("❌ 识别失败")
        else:
            print(f"❌ 请求失败: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")

def test_multiple_gestures():
    """测试多个手势数据"""
    
    gestures_data = [
        {
            "name": "石头手势",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.6, "confidence": 0.8},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.3, "y": 0.7, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.2, "y": 0.8, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.1, "y": 0.9, "confidence": 0.8},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.0, "y": 0.9, "confidence": 0.8}
            }
        },
        {
            "name": "剪刀手势",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 食指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 中指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85}   # 小指弯曲
            }
        },
        {
            "name": "布手势",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.6, "y": 0.2, "confidence": 0.8},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.7, "y": 0.2, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.8, "y": 0.2, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.9, "y": 0.2, "confidence": 0.8},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 1.0, "y": 0.2, "confidence": 0.8}
            }
        }
    ]
    
    print("\n🧪 测试多个手势数据")
    print("=" * 50)
    
    for gesture_test in gestures_data:
        print(f"\n🎮 测试: {gesture_test['name']}")
        print("-" * 30)
        
        try:
            response = requests.post(
                "http://192.168.1.26:8081/analyze_hand",
                json=gesture_test['data'],
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                gesture = result.get("gesture", "未知")
                confidence = result.get("confidence", 0.0)
                print(f"✅ 识别结果: {gesture} (置信度: {confidence:.2f})")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
        
        time.sleep(1)  # 避免请求过快

if __name__ == "__main__":
    test_ios_hand_data()
    test_multiple_gestures()
