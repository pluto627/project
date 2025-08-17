#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Arduino串口通信
直接与Arduino通信，验证机械臂控制
"""

import serial
import time
import sys

def test_arduino_serial():
    """测试Arduino串口通信"""
    port = '/dev/tty.usbserial-210'
    baudrate = 9600
    
    print(f"🔌 测试Arduino串口通信")
    print(f"📡 端口: {port}")
    print(f"⚡ 波特率: {baudrate}")
    print("=" * 50)
    
    try:
        # 连接Arduino
        print("🔗 正在连接Arduino...")
        ser = serial.Serial(port, baudrate, timeout=2)
        time.sleep(2)  # 等待Arduino重启
        
        print("✅ Arduino连接成功")
        
        # 测试命令列表
        test_commands = [
            ("ROCK", "石头"),
            ("PAPER", "布"), 
            ("SCISSORS", "剪刀"),
            ("RESET", "重置")
        ]
        
        for command, description in test_commands:
            print(f"\n🎮 测试命令: {command} ({description})")
            
            # 发送命令
            command_with_newline = f"{command}\n"
            print(f"📤 发送: {command_with_newline.strip()}")
            
            ser.write(command_with_newline.encode('utf-8'))
            ser.flush()
            
            # 等待响应
            time.sleep(0.5)
            
            # 读取响应
            if ser.in_waiting:
                response = ser.readline().decode('utf-8').strip()
                print(f"📥 收到: {response}")
            else:
                print("⚠️ 没有收到响应")
            
            # 等待机械臂动作完成
            time.sleep(2)
        
        # 关闭连接
        ser.close()
        print("\n✅ 串口测试完成")
        
    except serial.SerialException as e:
        print(f"❌ 串口连接失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    
    return True

def test_arduino_connection():
    """测试Arduino连接状态"""
    port = '/dev/tty.usbserial-210'
    baudrate = 9600
    
    print(f"🔍 检查Arduino连接状态...")
    
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(1)
        
        # 发送测试命令
        ser.write(b"RESET\n")
        ser.flush()
        
        time.sleep(0.5)
        
        if ser.in_waiting:
            response = ser.readline().decode('utf-8').strip()
            print(f"✅ Arduino响应: {response}")
            ser.close()
            return True
        else:
            print("⚠️ Arduino没有响应")
            ser.close()
            return False
            
    except Exception as e:
        print(f"❌ Arduino连接检查失败: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Arduino串口通信测试")
    print("=" * 50)
    
    # 首先检查连接
    if test_arduino_connection():
        print("\n✅ Arduino连接正常，开始测试命令...")
        test_arduino_serial()
    else:
        print("\n❌ Arduino连接失败，请检查硬件连接")
        sys.exit(1)
