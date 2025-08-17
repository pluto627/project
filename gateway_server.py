#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机械臂网关服务器
接收手机指令并转发给Arduino机械臂
"""

import serial
import json
import time
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

class ArduinoController:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.is_connected = False
        
    def connect(self):
        """连接到Arduino"""
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            time.sleep(2)  # 等待Arduino重启
            self.is_connected = True
            logger.info(f"✅ 成功连接到Arduino: {self.port}")
            return True
        except Exception as e:
            logger.error(f"❌ 连接Arduino失败: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """断开Arduino连接"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.is_connected = False
        logger.info("已断开Arduino连接")
    
    def send_command(self, command):
        """发送命令到Arduino"""
        if not self.is_connected or not self.serial_connection:
            logger.error("Arduino未连接")
            return False
        
        try:
            # 发送命令并等待响应
            command_with_newline = f"{command}\n"
            self.serial_connection.write(command_with_newline.encode('utf-8'))
            self.serial_connection.flush()
            
            # 等待响应
            time.sleep(0.1)
            if self.serial_connection.in_waiting:
                response = self.serial_connection.readline().decode('utf-8').strip()
                logger.info(f"Arduino响应: {response}")
            
            return True
        except Exception as e:
            logger.error(f"发送命令失败: {e}")
            return False

# 全局Arduino控制器
arduino_controller = ArduinoController()

# 手势映射
GESTURE_MAPPING = {
    "石头": "ROCK",
    "剪刀": "SCISSORS", 
    "布": "PAPER",
    "0": "0",  # 握拳
    "1": "1",  # 指向
    "2": "2",  # 胜利手势
    "3": "3",
    "4": "4", 
    "5": "5",  # 张开
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9"
}

@app.route('/status', methods=['GET'])
def status():
    """服务器状态检查"""
    return jsonify({
        "status": "running",
        "arduino_connected": arduino_controller.is_connected,
        "timestamp": time.time()
    })

@app.route('/connect', methods=['POST'])
def connect_arduino():
    """连接Arduino"""
    try:
        data = request.get_json()
        port = data.get('port', '/dev/ttyUSB0')
        
        arduino_controller.port = port
        success = arduino_controller.connect()
        
        return jsonify({
            "success": success,
            "message": "Arduino连接成功" if success else "Arduino连接失败"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"连接错误: {str(e)}"
        })

@app.route('/command', methods=['POST'])
def send_command():
    """发送通用命令"""
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        if not command:
            return jsonify({"success": False, "message": "命令不能为空"})
        
        success = arduino_controller.send_command(command)
        return jsonify({
            "success": success,
            "message": f"命令 '{command}' 发送{'成功' if success else '失败'}"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"发送命令错误: {str(e)}"
        })

@app.route('/gesture', methods=['POST'])
def send_gesture():
    """发送手势命令"""
    try:
        data = request.get_json()
        gesture = data.get('gesture', '')
        
        if not gesture:
            return jsonify({"success": False, "message": "手势不能为空"})
        
        # 映射手势到Arduino命令
        arduino_command = GESTURE_MAPPING.get(gesture, gesture)
        success = arduino_controller.send_command(arduino_command)
        
        return jsonify({
            "success": success,
            "message": f"手势 '{gesture}' 发送{'成功' if success else '失败'}",
            "arduino_command": arduino_command
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"发送手势错误: {str(e)}"
        })

@app.route('/rps', methods=['POST'])
def send_rps_gesture():
    """发送石头剪刀布手势"""
    try:
        data = request.get_json()
        gesture = data.get('gesture', '')
        
        if gesture not in ['石头', '剪刀', '布', 'ROCK', 'PAPER', 'SCISSORS']:
            return jsonify({"success": False, "message": "无效的手势"})
        
        # 映射到Arduino命令
        arduino_command = GESTURE_MAPPING.get(gesture, gesture)
        success = arduino_controller.send_command(arduino_command)
        
        return jsonify({
            "success": success,
            "message": f"RPS手势 '{gesture}' 发送{'成功' if success else '失败'}",
            "arduino_command": arduino_command
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"发送RPS手势错误: {str(e)}"
        })

@app.route('/number', methods=['POST'])
def send_number_gesture():
    """发送数字手势"""
    try:
        data = request.get_json()
        number = data.get('number', '')
        
        if not number.isdigit() or int(number) < 0 or int(number) > 9:
            return jsonify({"success": False, "message": "无效的数字手势"})
        
        success = arduino_controller.send_command(number)
        
        return jsonify({
            "success": success,
            "message": f"数字手势 '{number}' 发送{'成功' if success else '失败'}"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"发送数字手势错误: {str(e)}"
        })

@app.route('/reset', methods=['POST'])
def reset_hand():
    """重置机械手"""
    try:
        success = arduino_controller.send_command("RESET")
        return jsonify({
            "success": success,
            "message": "机械手重置命令发送成功" if success else "重置命令发送失败"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"重置错误: {str(e)}"
        })

@app.route('/openmax', methods=['POST'])
def open_hand_max():
    """机械手全部张开到最大"""
    try:
        success = arduino_controller.send_command("OPENMAX")
        return jsonify({
            "success": success,
            "message": "机械手全部张开到最大命令发送成功" if success else "张开命令发送失败"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"张开错误: {str(e)}"
        })

@app.route('/closemax', methods=['POST'])
def close_hand_max():
    """机械手全部握拳"""
    try:
        success = arduino_controller.send_command("CLOSEMAX")
        return jsonify({
            "success": success,
            "message": "机械手全部握拳命令发送成功" if success else "握拳命令发送失败"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"握拳错误: {str(e)}"
        })

@app.route('/analyze_hand', methods=['POST'])
def analyze_hand():
    """分析手部关键点数据并识别手势"""
    try:
        hand_data = request.get_json()
        
        # 这里实现手势识别逻辑
        # 基于手部关键点数据判断是石头、剪刀还是布
        gesture, confidence = analyze_hand_pose(hand_data)
        
        return jsonify({
            "gesture": gesture,
            "confidence": confidence,
            "success": True
        })
    except Exception as e:
        logger.error(f"手势分析错误: {e}")
        return jsonify({
            "gesture": "未知",
            "confidence": 0.0,
            "success": False,
            "error": str(e)
        })

def analyze_hand_pose(hand_data):
    """
    基于手部关键点数据识别手势 - 优化版本
    返回: (手势, 置信度)
    """
    try:
        logger.info(f"收到手部数据: {hand_data}")
        
        # 从iOS发送的数据中提取关键点
        # iOS使用Vision框架的VNHumanHandPoseObservationJointName
        thumb_tip = None
        index_tip = None
        middle_tip = None
        ring_tip = None
        pinky_tip = None
        
        # 查找对应的关键点
        for key, value in hand_data.items():
            if 'thumbTip' in str(key) or 'VNHumanHandPoseObservationJointName(_rawValue: VNHLKTTIP)' in str(key):
                thumb_tip = value
            elif 'indexTip' in str(key) or 'VNHumanHandPoseObservationJointName(_rawValue: VNHLKITIP)' in str(key):
                index_tip = value
            elif 'middleTip' in str(key) or 'VNHumanHandPoseObservationJointName(_rawValue: VNHLKMTIP)' in str(key):
                middle_tip = value
            elif 'ringTip' in str(key) or 'VNHumanHandPoseObservationJointName(_rawValue: VNHLKRTIP)' in str(key):
                ring_tip = value
            elif 'pinkyTip' in str(key) or 'VNHumanHandPoseObservationJointName(_rawValue: VNHLKPTIP)' in str(key):
                pinky_tip = value
        
        # 检查关键点是否存在
        if not all([thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]):
            logger.warning("关键点数据不完整")
            return "等待识别...", 0.0
        
        # 优化后的手指伸直判断
        fingers_info = []
        
        # 检查每个手指是否伸直（更精确的判断）
        for i, finger_tip in enumerate([thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]):
            confidence = finger_tip.get('confidence', 0)
            y_pos = finger_tip.get('y', 0.5)
            x_pos = finger_tip.get('x', 0.5)
            
            logger.info(f"手指{i}: Y={y_pos}, X={x_pos}, 置信度={confidence}")
            
            if confidence > 0.4:  # 提高置信度阈值，确保数据质量
                # 优化判断逻辑：考虑手指的相对位置和Y坐标
                is_extended = False
                
                if i == 0:  # 拇指 - 特殊处理
                    # 拇指的判断更复杂，需要结合X和Y坐标
                    is_extended = y_pos < 0.6 and x_pos > 0.3
                elif i == 4:  # 小拇指 - 特殊处理
                    # 小拇指通常比其他手指短，需要更宽松的阈值
                    is_extended = y_pos < 0.95  # 大幅放宽阈值，让小拇指初始状态为180度伸直
                else:  # 其他手指（食指、中指、无名指）
                    # 其他手指主要看Y坐标，但阈值更精确
                    is_extended = y_pos < 0.45  # 降低阈值，更严格
                
                fingers_info.append({
                    'extended': is_extended,
                    'confidence': confidence,
                    'y_pos': y_pos,
                    'x_pos': x_pos
                })
                logger.info(f"手指{i} {'伸直' if is_extended else '弯曲'}")
            else:
                fingers_info.append({
                    'extended': False,
                    'confidence': confidence,
                    'y_pos': y_pos,
                    'x_pos': x_pos
                })
                logger.info(f"手指{i} 置信度太低")
        
        extended_count = sum(1 for finger in fingers_info if finger['extended'])
        extended_fingers = [i for i, finger in enumerate(fingers_info) if finger['extended']]
        
        logger.info(f"伸直的手指数量: {extended_count}")
        logger.info(f"伸直的手指索引: {extended_fingers}")
        logger.info(f"手指状态: {[finger['extended'] for finger in fingers_info]}")
        
        # 优化后的手势识别逻辑
        if extended_count == 0:
            # 所有手指都弯曲 - 石头
            logger.info("识别为: 石头")
            return "石头", 0.9
        elif extended_count == 2:
            # 两个手指伸直 - 剪刀
            # 检查是否是食指和中指（典型的剪刀手势）
            if 1 in extended_fingers and 2 in extended_fingers:
                logger.info("识别为: 剪刀 (食指+中指)")
                return "剪刀", 0.95
            elif 0 in extended_fingers and 1 in extended_fingers:
                logger.info("识别为: 剪刀 (拇指+食指)")
                return "剪刀", 0.9
            else:
                logger.info("识别为: 剪刀 (其他两个手指)")
                return "剪刀", 0.85
        elif extended_count == 1:
            # 只有一个手指伸直 - 可能是剪刀的开始或石头的变化
            if 1 in extended_fingers:  # 只有食指伸直
                logger.info("识别为: 剪刀 (只有食指)")
                return "剪刀", 0.7
            else:
                logger.info("识别为: 石头 (变化中)")
                return "石头", 0.6
        elif extended_count >= 3:
            # 三个或更多手指伸直 - 布
            logger.info("识别为: 布")
            return "布", 0.9
        else:
            logger.info(f"无法识别手势，伸直手指数: {extended_count}")
            return "未知", 0.3
            
    except Exception as e:
        logger.error(f"手势分析失败: {e}")
        return "未知", 0.0

def auto_connect_arduino():
    """自动尝试连接Arduino"""
    common_ports = [
        '/dev/tty.usbserial-210',  # 你的Arduino设备
        '/dev/ttyUSB0',
        '/dev/ttyUSB1', 
        '/dev/ttyACM0',
        '/dev/ttyACM1',
        'COM1',
        'COM2',
        'COM3',
        'COM4'
    ]
    
    for port in common_ports:
        logger.info(f"尝试连接端口: {port}")
        arduino_controller.port = port
        if arduino_controller.connect():
            return True
    
    logger.warning("无法自动连接Arduino，请手动连接")
    return False

if __name__ == '__main__':
    # 启动时尝试连接Arduino
    auto_connect_arduino()
    
    # 启动Flask服务器
    logger.info("🚀 启动机械臂网关服务器...")
    logger.info("📱 手机端连接地址: http://[你的电脑IP]:8081")
    logger.info("🔧 Arduino连接状态: " + ("已连接" if arduino_controller.is_connected else "未连接"))
    
    app.run(host='0.0.0.0', port=8081, debug=True)
