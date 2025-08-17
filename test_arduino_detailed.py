#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细的Arduino测试脚本
诊断Arduino命令处理问题
"""

import serial
import time

def test_arduino_detailed():
    """详细测试Arduino"""
    port = '/dev/tty.usbserial-210'
    baudrate = 9600
    
    print("🔍 详细Arduino测试")
    print("=" * 50)
    
    try:
        # 连接Arduino
        print("🔗 连接Arduino...")
        ser = serial.Serial(port, baudrate, timeout=2)
        time.sleep(2)
        
        print("✅ Arduino连接成功")
        
        # 清空缓冲区
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # 测试命令列表
        test_commands = [
            ("ROCK", "石头"),
            ("PAPER", "布"), 
            ("SCISSORS", "剪刀"),
            ("RESET", "重置")
        ]
        
        for command, description in test_commands:
            print(f"\n🎮 测试: {description} ({command})")
            
            # 清空缓冲区
            ser.reset_input_buffer()
            
            # 发送命令
            command_with_newline = f"{command}\n"
            print(f"📤 发送: {command_with_newline.strip()}")
            
            ser.write(command_with_newline.encode('utf-8'))
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
                    
                    # 检查特定响应
                    if "识别为RPS手势" in response:
                        print("   ✅ 正确识别为RPS手势")
                    elif "动作:" in response:
                        print("   ✅ 执行了动作")
                    elif "无效" in response:
                        print("   ❌ 命令识别失败")
                    elif "收到命令" in response:
                        print("   📥 收到命令")
            else:
                print("⚠️ 没有收到响应")
            
            # 等待动作完成
            time.sleep(2)
        
        # 关闭连接
        ser.close()
        print("\n✅ 详细测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_individual_commands():
    """测试单个命令"""
    port = '/dev/tty.usbserial-210'
    baudrate = 9600
    
    print("\n🔧 单个命令测试")
    print("=" * 50)
    
    try:
        ser = serial.Serial(port, baudrate, timeout=2)
        time.sleep(2)
        
        # 测试单个命令
        commands = [
            "ROCK",
            "PAPER", 
            "SCISSORS",
            "RESET"
        ]
        
        for command in commands:
            print(f"\n🎯 测试命令: {command}")
            
            # 清空缓冲区
            ser.reset_input_buffer()
            
            # 发送命令
            ser.write(f"{command}\n".encode('utf-8'))
            ser.flush()
            
            # 等待响应
            time.sleep(1)
            
            # 读取响应
            if ser.in_waiting:
                response = ser.readline().decode('utf-8').strip()
                print(f"📥 响应: {response}")
                
                # 分析响应
                if "识别为RPS手势" in response:
                    print("✅ 命令识别正确")
                elif "动作:" in response:
                    print("✅ 执行了动作")
                elif "无效" in response:
                    print("❌ 命令识别失败")
                else:
                    print("⚠️ 未知响应")
            else:
                print("⚠️ 无响应")
            
            time.sleep(2)
        
        ser.close()
        
    except Exception as e:
        print(f"❌ 单个命令测试失败: {e}")

if __name__ == "__main__":
    test_arduino_detailed()
    test_individual_commands()
