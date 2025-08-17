#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
舵机诊断脚本
检查每个舵机的连接状态
"""

import serial
import time

def diagnose_servos():
    """诊断舵机状态"""
    port = '/dev/tty.usbserial-210'
    baudrate = 9600
    
    print("🔧 舵机诊断工具")
    print("=" * 50)
    print("舵机引脚配置:")
    print("- 舵机1 (小拇指): 引脚3")
    print("- 舵机2 (无名指): 引脚4")
    print("- 舵机3 (中指): 引脚5")
    print("- 舵机4 (食指): 引脚6")
    print("- 舵机5 (大拇指): 引脚7")
    print("- 舵机6 (手腕): 引脚8")
    print("=" * 50)
    
    try:
        # 连接Arduino
        print("🔗 连接Arduino...")
        ser = serial.Serial(port, baudrate, timeout=2)
        time.sleep(2)
        
        print("✅ Arduino连接成功")
        
        # 测试每个舵机
        servo_tests = [
            ("RESET", "重置 - 测试所有舵机"),
            ("ROCK", "石头 - 测试握拳动作"),
            ("PAPER", "布 - 测试张开动作"),
            ("SCISSORS", "剪刀 - 测试特定手指")
        ]
        
        for command, description in servo_tests:
            print(f"\n🎮 测试: {description}")
            print(f"📤 发送命令: {command}")
            
            # 发送命令
            ser.write(f"{command}\n".encode('utf-8'))
            ser.flush()
            
            # 等待响应
            time.sleep(1)
            
            # 读取所有可用响应
            responses = []
            while ser.in_waiting:
                response = ser.readline().decode('utf-8').strip()
                if response:
                    responses.append(response)
            
            if responses:
                print("📥 Arduino响应:")
                for response in responses:
                    print(f"   {response}")
                    
                    # 检查舵机错误
                    if "disconnected" in response.lower():
                        print(f"   ⚠️ 舵机连接问题!")
                    elif "error" in response.lower():
                        print(f"   ❌ 舵机错误!")
            else:
                print("⚠️ 没有收到响应")
            
            # 等待动作完成
            time.sleep(3)
        
        # 关闭连接
        ser.close()
        print("\n✅ 诊断完成")
        
    except Exception as e:
        print(f"❌ 诊断失败: {e}")

def test_individual_servos():
    """测试单个舵机"""
    port = '/dev/tty.usbserial-210'
    baudrate = 9600
    
    print("\n🔧 单个舵机测试")
    print("=" * 50)
    
    try:
        ser = serial.Serial(port, baudrate, timeout=2)
        time.sleep(2)
        
        # 测试单个舵机命令
        servo_commands = [
            ("SERVO:0:90", "舵机1 (小拇指) 到90度"),
            ("SERVO:1:90", "舵机2 (无名指) 到90度"),
            ("SERVO:2:90", "舵机3 (中指) 到90度"),
            ("SERVO:3:90", "舵机4 (食指) 到90度"),
            ("SERVO:4:90", "舵机5 (大拇指) 到90度"),
            ("SERVO:5:90", "舵机6 (手腕) 到90度")
        ]
        
        for command, description in servo_commands:
            print(f"\n🎯 {description}")
            print(f"📤 发送: {command}")
            
            ser.write(f"{command}\n".encode('utf-8'))
            ser.flush()
            
            time.sleep(1)
            
            if ser.in_waiting:
                response = ser.readline().decode('utf-8').strip()
                print(f"📥 响应: {response}")
            else:
                print("⚠️ 无响应")
            
            time.sleep(2)
        
        ser.close()
        
    except Exception as e:
        print(f"❌ 单个舵机测试失败: {e}")

if __name__ == "__main__":
    diagnose_servos()
    test_individual_servos()
