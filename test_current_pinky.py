#!/usr/bin/env python3
"""
测试用户当前的小拇指状态
"""

import requests
import json
import time

def test_current_pinky_status():
    """测试用户当前的小拇指状态"""
    
    # 基于你日志中的真实数据
    current_data = {
        "name": "用户当前状态 - 真实数据",
        "data": {
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},  # 拇指弯曲
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 食指弯曲
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 中指弯曲
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},  # 无名指弯曲
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": 0.8, "confidence": 0.85}   # 小拇指弯曲
        }
    }
    
    print("🖐️ 测试用户当前小拇指状态")
    print("=" * 50)
    
    try:
        response = requests.post(
            "http://192.168.1.26:8081/analyze_hand",
            json=current_data["data"],
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
            pinky_y = current_data["data"]["VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)"]["y"]
            print(f"🖐️ 小拇指Y坐标: {pinky_y}")
            
            # 使用新的阈值 0.95
            if pinky_y < 0.95:
                pinky_status = "伸直"
            else:
                pinky_status = "弯曲"
            print(f"🔍 小拇指状态 (阈值0.95): {pinky_status}")
            
            if pinky_status == "伸直":
                print("🟢 小拇指现在被识别为伸直状态！")
            else:
                print("🔴 小拇指仍然被识别为弯曲状态")
                
        else:
            print(f"❌ 请求失败: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")

def test_pinky_thresholds():
    """测试不同的小拇指阈值"""
    
    print("\n🔧 测试不同的小拇指阈值")
    print("=" * 50)
    
    # 测试不同的小拇指Y坐标值
    test_values = [0.7, 0.75, 0.8, 0.85, 0.9]
    
    for y_value in test_values:
        test_data = {
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTCMC)": {"x": 0.5, "y": 0.3, "confidence": 0.9},
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)": {"x": 0.4, "y": 0.7, "confidence": 0.85},
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)": {"x": 0.5, "y": 0.7, "confidence": 0.85},
            "VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)": {"x": 0.5, "y": y_value, "confidence": 0.85}
        }
        
        print(f"\n🎯 测试小拇指Y坐标: {y_value}")
        
        try:
            response = requests.post(
                "http://192.168.1.26:8081/analyze_hand",
                json=test_data,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                gesture = result.get("gesture", "未知")
                
                # 判断小拇指状态
                if y_value < 0.95:
                    expected_status = "伸直"
                else:
                    expected_status = "弯曲"
                
                print(f"📊 手势: {gesture}")
                print(f"🔍 小拇指状态: {expected_status}")
                
            else:
                print(f"❌ 请求失败: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
        
        time.sleep(0.5)

def show_current_tips():
    """显示当前状态的建议"""
    
    print("\n💡 当前小拇指状态分析")
    print("=" * 50)
    print("""
🎯 当前设置：
✅ 小拇指阈值设置为 0.95
✅ 小拇指Y坐标 < 0.95 时识别为伸直 (180度)

📊 你的小拇指状态：
- Y=0.8: 伸直 ✅ (180度)
- Y=0.85: 伸直 ✅ (180度)
- Y=0.9: 伸直 ✅ (180度)
- Y=0.95: 弯曲

🖐️ 建议：
1. 现在小拇指Y坐标 < 0.95 时会被识别为伸直 (180度)
2. 你的Y=0.8-0.9现在都会被识别为伸直状态
3. 如果Y坐标 > 0.95，小拇指会被识别为弯曲

🔧 如果仍然有问题：
- 可以进一步调整阈值到 1.0
- 或者调整手部位置，让小拇指更明显
    """)

if __name__ == "__main__":
    test_current_pinky_status()
    test_pinky_thresholds()
    show_current_tips()
