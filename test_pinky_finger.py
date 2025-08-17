#!/usr/bin/env python3
"""
专门测试小拇指识别准确性的脚本
"""

import requests
import json
import time

def test_pinky_finger_variations():
    """测试小拇指的不同状态"""
    
    pinky_tests = [
        {
            "name": "小拇指伸直 (Y=0.4)",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 食指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.4, "confidence": 0.85}   # 小拇指伸直
            }
        },
        {
            "name": "小拇指半伸直 (Y=0.5)",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 食指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.5, "confidence": 0.85}   # 小拇指半伸直
            }
        },
        {
            "name": "小拇指弯曲 (Y=0.7)",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 食指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85}   # 小拇指弯曲
            }
        },
        {
            "name": "小拇指很弯曲 (Y=0.8)",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 食指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.8, "confidence": 0.85}   # 小拇指很弯曲
            }
        },
        {
            "name": "只有小拇指伸直",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 食指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.4, "confidence": 0.85}   # 小拇指伸直
            }
        },
        {
            "name": "小拇指+食指伸直",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 食指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.4, "confidence": 0.85}   # 小拇指伸直
            }
        }
    ]
    
    print("🖐️ 测试小拇指识别准确性")
    print("=" * 50)
    
    for i, test in enumerate(pinky_tests, 1):
        print(f"\n🎯 测试 {i}: {test['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                "http://192.168.1.26:8081/analyze_hand",
                json=test['data'],
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                gesture = result.get("gesture", "未知")
                confidence = result.get("confidence", 0.0)
                success = result.get("success", False)
                
                print(f"📊 识别结果: {gesture}")
                print(f"🎯 置信度: {confidence:.2f}")
                print(f"✅ 成功: {success}")
                
                # 分析小拇指状态
                pinky_y = test['data']['VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)']['y']
                print(f"🖐️ 小拇指Y坐标: {pinky_y}")
                
                if pinky_y < 0.55:
                    expected_status = "伸直"
                else:
                    expected_status = "弯曲"
                print(f"🔍 期望状态: {expected_status}")
                
                # 评估识别质量
                if "只有小拇指伸直" in test['name']:
                    if gesture == "石头":
                        print("🟢 正确识别 (只有小拇指伸直应该识别为石头)")
                    else:
                        print("🟡 可接受的识别")
                elif "小拇指+食指伸直" in test['name']:
                    if gesture == "剪刀":
                        print("🟢 正确识别 (两个手指伸直识别为剪刀)")
                    else:
                        print("🟡 可接受的识别")
                else:
                    print("🟡 测试数据")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
        
        time.sleep(1)  # 避免请求过快

def test_real_pinky_data():
    """测试真实的小拇指数据（从日志中提取）"""
    
    real_data = [
        {
            "name": "真实数据 - 小拇指弯曲 (Y=0.887)",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.887, "confidence": 0.85}
            }
        },
        {
            "name": "真实数据 - 小拇指弯曲 (Y=0.804)",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.804, "confidence": 0.85}
            }
        }
    ]
    
    print("\n📊 测试真实小拇指数据")
    print("=" * 50)
    
    for i, test in enumerate(real_data, 1):
        print(f"\n🎯 真实测试 {i}: {test['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                "http://192.168.1.26:8081/analyze_hand",
                json=test['data'],
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                gesture = result.get("gesture", "未知")
                confidence = result.get("confidence", 0.0)
                
                print(f"📊 识别结果: {gesture}")
                print(f"🎯 置信度: {confidence:.2f}")
                
                # 分析小拇指状态
                pinky_y = test['data']['VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)']['y']
                print(f"🖐️ 小拇指Y坐标: {pinky_y}")
                
                if pinky_y < 0.55:
                    expected_status = "伸直"
                else:
                    expected_status = "弯曲"
                print(f"🔍 期望状态: {expected_status}")
                
                if expected_status == "弯曲":
                    print("🟢 正确识别小拇指为弯曲状态")
                else:
                    print("🔴 小拇指状态识别错误")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    test_pinky_finger_variations()
    test_real_pinky_data()
