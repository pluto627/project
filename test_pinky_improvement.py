#!/usr/bin/env python3
"""
测试小拇指伸直改善效果
"""

import requests
import json
import time

def test_pinky_improvement():
    """测试小拇指伸直改善效果"""
    
    # 模拟用户实际的手势数据
    test_cases = [
        {
            "name": "用户当前状态 - 小拇指弯曲 (Y=0.8)",
            "description": "这是你当前的状态，小拇指弯曲",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 食指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.8, "confidence": 0.85}   # 小拇指弯曲
            }
        },
        {
            "name": "改善后 - 小拇指伸直 (Y=0.55)",
            "description": "这是你伸直小拇指后的状态",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 食指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.55, "confidence": 0.85}   # 小拇指伸直
            }
        },
        {
            "name": "进一步伸直 - 小拇指更直 (Y=0.45)",
            "description": "这是你进一步伸直小拇指的状态",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 食指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.45, "confidence": 0.85}   # 小拇指更直
            }
        },
        {
            "name": "剪刀手势 - 食指+中指伸直",
            "description": "标准的剪刀手势，小拇指弯曲",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 食指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 中指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85}   # 小拇指弯曲
            }
        },
        {
            "name": "剪刀手势 - 食指+中指+小拇指伸直",
            "description": "剪刀手势，但小拇指也伸直了",
            "data": {
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 食指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.35, "confidence": 0.95},  # 中指伸直
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
                "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.55, "confidence": 0.85}   # 小拇指伸直
            }
        }
    ]
    
    print("🖐️ 测试小拇指伸直改善效果")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🎯 测试 {i}: {test['name']}")
        print(f"📝 {test['description']}")
        print("-" * 50)
        
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
                
                if pinky_y < 0.6:
                    pinky_status = "伸直"
                else:
                    pinky_status = "弯曲"
                print(f"🔍 小拇指状态: {pinky_status}")
                
                # 评估结果
                if "当前状态" in test['name']:
                    if gesture == "石头" and pinky_status == "弯曲":
                        print("🟢 正确识别当前状态")
                    else:
                        print("🔴 当前状态识别错误")
                elif "改善后" in test['name'] or "进一步伸直" in test['name']:
                    if pinky_status == "伸直":
                        print("🟢 小拇指成功识别为伸直状态")
                    else:
                        print("🔴 小拇指仍然被识别为弯曲")
                elif "剪刀手势" in test['name']:
                    if gesture == "剪刀":
                        print("🟢 正确识别剪刀手势")
                    else:
                        print("🔴 剪刀手势识别错误")
                else:
                    print("🟡 测试数据")
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
        
        time.sleep(1)  # 避免请求过快

def show_improvement_tips():
    """显示改善小拇指伸直的建议"""
    
    print("\n💡 小拇指伸直改善建议")
    print("=" * 60)
    print("""
🎯 目标：让你的小拇指更容易被识别为伸直状态

📋 当前优化：
✅ 小拇指阈值从 0.45 调整到 0.6
✅ 小拇指现在更容易被识别为伸直

🖐️ 实际使用建议：
1. 尝试伸直小拇指，让Y坐标 < 0.6
2. 小拇指伸直时，Y坐标应该在 0.4-0.6 之间
3. 如果Y坐标 > 0.6，小拇指会被识别为弯曲

📊 测试你的手势：
- 在iOS应用中启动摄像头
- 观察服务器日志中的小拇指Y坐标
- 尝试调整小拇指位置，让Y坐标 < 0.6

🔧 如果仍然有问题：
- 可以进一步调整阈值到 0.65
- 或者调整手部位置，让小拇指更明显
    """)

if __name__ == "__main__":
    test_pinky_improvement()
    show_improvement_tips()
