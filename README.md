# 机械臂手势控制项目

这是一个完整的机械臂手势控制系统，包含手机端手势识别、电脑网关服务器和Arduino机械臂控制。

## 🎯 项目功能

- **实时手势识别**: 使用手机摄像头识别石头、剪刀、布手势
- **石头剪刀布游戏**: 机械臂总是获胜的智能游戏
- **实时摄像头预览**: 流畅的摄像头预览界面
- **电脑网关服务器**: 接收手机指令并转发给Arduino
- **Arduino机械臂控制**: 精确的舵机控制

## 📁 代码分类说明

### 🔧 Arduino代码版本

#### 第一版代码 (基础版本)
- `hand_control_nano_parallel.ino` - 基础机械手控制器，支持数字手势0-9和石头剪刀布

#### 第二版代码 (修复版本)
- `hand_control_nano_parallel_fixed.ino` - 修复版，添加了舵机连接检测和初始化功能
- `hand_control_nano_parallel_fixed_v2.ino` - 修复版V2，进一步优化了舵机控制逻辑
- `hand_control_nano_parallel_fixed_v3.ino` - 修复版V3，最新稳定版本，包含完整的错误处理和优化

### 🐍 Python代码分类

#### 核心服务器代码
- `gateway_server.py` - 主要的Flask网关服务器，处理手机端请求并控制Arduino
- `setup.py` - 项目安装和配置脚本

#### 测试和诊断代码
- `test_arduino_serial.py` - Arduino串口通信测试
- `test_arduino_detailed.py` - 详细的Arduino功能测试
- `test_http_connection.py` - HTTP连接测试
- `test_system.py` - 系统整体功能测试
- `diagnose_servos.py` - 舵机诊断工具

#### 手势识别测试
- `test_gesture_recognition.py` - 手势识别算法测试
- `test_ios_hand_data.py` - iOS手部数据处理测试

#### 机械臂控制测试
- `test_mechanical_arm.py` - 机械臂基础控制测试
- `test_manual_buttons.py` - 手动按钮控制测试

#### 石头剪刀布游戏测试
- `test_rps_fix.py` - 石头剪刀布游戏修复测试
- `test_scissors_accuracy.py` - 剪刀手势精度测试

#### 手指控制测试
- `test_pinky_finger.py` - 小拇指控制测试
- `test_pinky_180_degree.py` - 小拇指180度控制测试
- `test_pinky_improvement.py` - 小拇指控制改进测试
- `test_current_pinky.py` - 当前小拇指控制状态测试

#### 手势控制测试
- `test_openmax.py` - 最大张开角度测试
- `test_closemax.py` - 最大闭合角度测试

### 📱 iOS应用代码
- `hand/` - iOS应用源代码目录
  - `ContentView.swift` - 主界面
  - `HandController.swift` - 手势控制器
  - `SimpleCameraView.swift` - 摄像头视图
  - `SimpleGestureRecognitionView.swift` - 手势识别视图
  - `CameraDataView.swift` - 摄像头数据显示视图

### 📋 配置和文档
- `requirements.txt` - Python依赖包列表
- `start_server.sh` - 服务器启动脚本
- `硬件检查指南.md` - 硬件连接和检查指南
- `项目总结.md` - 项目开发总结文档

## 🚀 快速开始

### 1. 硬件准备
1. 连接Arduino Nano到电脑
2. 连接6个舵机到对应引脚
3. 上传最新的Arduino代码 `hand_control_nano_parallel_fixed_v3.ino`

### 2. 电脑端设置
```bash
# 克隆项目
git clone https://github.com/pluto627/project.git
cd project

# 安装Python依赖
pip3 install -r requirements.txt

# 启动网关服务器
./start_server.sh
```

### 3. 手机端设置
1. 打开Xcode项目`hand.xcodeproj`
2. 修改`HandController.swift`中的服务器IP地址
3. 编译并运行到iPhone

### 4. 网络配置
1. 确保手机和电脑在同一个WiFi网络
2. 获取电脑IP地址
3. 在手机端更新服务器地址

## 📋 使用说明

### 启动顺序
1. 启动电脑网关服务器
2. 确保Arduino已连接并上传代码
3. 在手机上启动应用
4. 点击"启动摄像头"
5. 点击"开始游戏"

### 游戏规则
- 玩家通过摄像头做出石头、剪刀、布手势
- 机械臂会自动识别并做出获胜手势
- 机械臂总是获胜（这是设计特性）
- 实时显示游戏统计

### 手势识别
- 将手掌放在摄像头前
- 做出清晰的手势
- 等待AI识别（需要1-2秒稳定时间）
- 查看识别结果和置信度

## 🔧 配置说明

### 修改服务器地址
在`HandController.swift`中修改：
```swift
private var serverURL = "http://你的电脑IP:8081"
```

### 修改Arduino端口
在`gateway_server.py`中修改：
```python
arduino_controller = ArduinoController(port='/dev/ttyUSB0')
```

### 调整手势识别参数
在`SimpleGestureRecognitionView.swift`中调整：
- 置信度阈值: `confidence < 0.4`
- 稳定性要求: `gestureStabilityCount >= 2`
- 识别冷却时间: `gestureCooldown: TimeInterval = 0.8`

## 🐛 故障排除

### 连接问题
1. 检查网络连接
2. 确认IP地址正确
3. 检查防火墙设置
4. 重启网关服务器

### Arduino连接问题
1. 检查串口连接
2. 确认Arduino代码已上传
3. 检查舵机连接
4. 查看串口日志

### 手势识别问题
1. 确保光线充足
2. 保持手势稳定
3. 调整摄像头距离
4. 检查置信度设置

## 📊 技术架构

```
手机端 (iOS Swift)
    ↓ HTTP请求
电脑网关服务器 (Python Flask)
    ↓ 串口通信
Arduino机械臂 (C++)
```

### 数据流
1. 手机摄像头捕获视频
2. Vision框架检测手部关键点
3. 发送关键点数据到Python服务器
4. Python服务器分析手势
5. 发送命令到Arduino
6. Arduino控制舵机执行手势

## 🔮 未来改进

- [ ] 支持更多手势类型
- [ ] 添加手势录制功能
- [ ] 实现手势序列播放
- [ ] 添加语音控制
- [ ] 优化识别算法
- [ ] 添加手势教学功能

## 📄 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系方式

如有问题，请通过以下方式联系：
- GitHub: [pluto627](https://github.com/pluto627)

---

**注意**: 请确保在使用前仔细阅读所有说明，并按照正确的顺序进行设置。
