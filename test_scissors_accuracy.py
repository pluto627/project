#!/usr/bin/env python3
"""
专门测试剪刀手势识别准确性的脚本
"""

import requests
import json
import time

def test_scissors_variations():
    """测试剪刀手势的不同变体"""
    
    scissors_variations = [
        {
            "name": "标准剪刀 (食指+中指)",
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
            "name": "拇指+食指剪刀",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.4, "confidence": 0.85},  # 拇指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 食指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85}   # 小指弯曲
            }
        },
        {
            "name": "只有食指伸直",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 食指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85}   # 小指弯曲
            }
        },
        {
            "name": "食指+中指+无名指 (可能误识别为布)",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 食指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 中指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.35, "confidence": 0.85},  # 无名指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85}   # 小指弯曲
            }
        },
        {
            "name": "低置信度剪刀",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.35},  # 拇指弯曲，低置信度
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.35, "confidence": 0.45},  # 食指伸直，低置信度
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.35, "confidence": 0.45},  # 中指伸直，低置信度
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.35},  # 无名指弯曲，低置信度
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.35}   # 小指弯曲，低置信度
            }
        }
    ]
    
    print("✂️ 测试剪刀手势识别准确性")
    print("=" * 50)
    
    for i, variation in enumerate(scissors_variations, 1):
        print(f"\n🎯 测试 {i}: {variation['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                "http://192.168.1.26:8081/analyze_hand",
                json=variation['data'],
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
                
                # 评估识别质量
                if gesture == "剪刀":
                    if confidence >= 0.9:
                        print("🟢 优秀识别")
                    elif confidence >= 0.7:
                        print("🟡 良好识别")
                    else:
                        print("🟠 一般识别")
                elif gesture == "石头" and "只有食指" in variation['name']:
                    print("🟡 可接受的识别 (只有食指可能被识别为石头)")
                elif gesture == "布" and "食指+中指+无名指" in variation['name']:
                    print("🟡 可接受的识别 (三个手指可能被识别为布)")
                else:
                    print("🔴 识别错误")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
        
        time.sleep(1)  # 避免请求过快

def test_edge_cases():
    """测试边界情况"""
    
    edge_cases = [
        {
            "name": "所有手指都弯曲 (应该是石头)",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.8, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.8, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.8, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.8, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.8, "confidence": 0.85}
            }
        },
        {
            "name": "所有手指都伸直 (应该是布)",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.2, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.2, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.2, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.2, "confidence": 0.85},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.2, "confidence": 0.85}
            }
        }
    ]
    
    print("\n🔍 测试边界情况")
    print("=" * 50)
    
    for i, case in enumerate(edge_cases, 1):
        print(f"\n🎯 边界测试 {i}: {case['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                "http://192.168.1.26:8081/analyze_hand",
                json=case['data'],
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                gesture = result.get("gesture", "未知")
                confidence = result.get("confidence", 0.0)
                
                print(f"📊 识别结果: {gesture}")
                print(f"🎯 置信度: {confidence:.2f}")
                
                # 评估识别质量
                expected = "石头" if "弯曲" in case['name'] else "布"
                if gesture == expected:
                    print("🟢 正确识别")
                else:
                    print("🔴 识别错误")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    test_scissors_variations()
    test_edge_cases()
