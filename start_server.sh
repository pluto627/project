#!/bin/bash

# 机械臂网关服务器启动脚本

echo "🚀 启动机械臂网关服务器..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查依赖是否安装
echo "📦 检查Python依赖..."
if ! python3 -c "import flask, serial, requests" 2>/dev/null; then
    echo "📥 安装Python依赖..."
    pip3 install -r requirements.txt
fi

# 获取本机IP地址
IP_ADDRESS=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

echo "🌐 本机IP地址: $IP_ADDRESS"
echo "📱 手机端连接地址: http://$IP_ADDRESS:8081"
echo "🔧 请确保手机和电脑在同一个WiFi网络下"
echo ""

# 启动服务器
echo "✅ 启动服务器..."
echo "🔧 使用虚拟环境..."
source venv/bin/activate
python3 gateway_server.py
