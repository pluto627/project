//
//  SimpleGestureRecognitionView.swift
//  hand
//
//  Created by pluto guo on 8/16/25.
//

import SwiftUI
import AVFoundation
import Vision

struct SimpleGestureRecognitionView: View {
    @StateObject private var cameraManager = GestureCameraManager()
    @StateObject private var handController = HandController()
    
    // 游戏状态
    @State private var currentGesture: String = "等待识别..."
    @State private var gameResult: String = ""
    @State private var isGameActive = false
    @State private var showingCamera = false
    @State private var gestureCount = 0
    @State private var confidence: Float = 0.0
    @State private var lastValidGesture: String = ""
    @State private var gestureStabilityCount = 0
    @State private var isProcessing = false
    
    // 游戏统计
    @State private var playerScore = 0
    @State private var robotScore = 0
    @State private var totalGames = 0
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // 摄像头预览区域
                ZStack {
                    if showingCamera {
                        GestureCameraPreviewView(cameraManager: cameraManager)
                            .frame(height: 350)
                            .cornerRadius(16)
                            .overlay(
                                RoundedRectangle(cornerRadius: 16)
                                    .stroke(Color.blue, lineWidth: 3)
                            )
                            .shadow(radius: 10)
                    } else {
                        RoundedRectangle(cornerRadius: 16)
                            .fill(Color.gray.opacity(0.2))
                            .frame(height: 350)
                            .overlay(
                                VStack(spacing: 20) {
                                    Image(systemName: "camera.fill")
                                        .font(.system(size: 60))
                                        .foregroundColor(.gray)
                                    Text("点击启动摄像头开始游戏")
                                        .font(.headline)
                                        .foregroundColor(.gray)
                                    Text("识别石头、剪刀、布手势")
                                        .font(.subheadline)
                                        .foregroundColor(.gray.opacity(0.8))
                                }
                            )
                    }
                    
                    // 实时状态指示器
                    if showingCamera {
                        VStack {
                            HStack {
                                Circle()
                                    .fill(Color.green)
                                    .frame(width: 10, height: 10)
                                Text("实时识别中")
                                    .font(.caption)
                                    .foregroundColor(.white)
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 5)
                                    .background(Color.black.opacity(0.7))
                                    .cornerRadius(8)
                                Spacer()
                            }
                            Spacer()
                        }
                        .padding(12)
                    }
                }
                
                // 手势识别结果
                VStack(spacing: 15) {
                    Text("识别到的手势")
                        .font(.headline)
                        .foregroundColor(.primary)
                    
                    Text(currentGesture)
                        .font(.system(size: 32, weight: .bold))
                        .foregroundColor(.blue)
                        .padding(.horizontal, 30)
                        .padding(.vertical, 15)
                        .background(
                            RoundedRectangle(cornerRadius: 12)
                                .fill(Color.blue.opacity(0.1))
                                .overlay(
                                    RoundedRectangle(cornerRadius: 12)
                                        .stroke(Color.blue, lineWidth: 2)
                                )
                        )
                    
                    // 处理状态和置信度
                    HStack {
                        if isProcessing {
                            HStack(spacing: 8) {
                                ProgressView()
                                    .scaleEffect(0.8)
                                Text("AI分析中...")
                                    .font(.caption)
                                    .foregroundColor(.orange)
                            }
                        } else {
                            HStack(spacing: 8) {
                                Image(systemName: "brain.head.profile")
                                    .foregroundColor(.green)
                                Text("置信度: \(Int(confidence * 100))%")
                                    .font(.caption)
                                    .foregroundColor(.green)
                            }
                        }
                        
                        Spacer()
                        
                        if gestureStabilityCount > 0 {
                            HStack(spacing: 8) {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundColor(.green)
                                Text("稳定性: \(gestureStabilityCount)")
                                    .font(.caption)
                                    .foregroundColor(.green)
                            }
                        }
                    }
                    .padding(.horizontal)
                }
                
                // 游戏结果
                if !gameResult.isEmpty {
                    VStack(spacing: 10) {
                        Text("游戏结果")
                            .font(.headline)
                            .foregroundColor(.primary)
                        
                        Text(gameResult)
                            .font(.title2)
                            .fontWeight(.semibold)
                            .foregroundColor(.green)
                            .padding(.horizontal, 20)
                            .padding(.vertical, 12)
                            .background(
                                RoundedRectangle(cornerRadius: 10)
                                    .fill(Color.green.opacity(0.1))
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 10)
                                            .stroke(Color.green, lineWidth: 2)
                                    )
                            )
                    }
                }
                
                // 游戏统计
                if totalGames > 0 {
                    HStack(spacing: 30) {
                        VStack {
                            Text("玩家")
                                .font(.caption)
                                .foregroundColor(.gray)
                            Text("\(playerScore)")
                                .font(.title2)
                                .fontWeight(.bold)
                                .foregroundColor(.blue)
                        }
                        
                        VStack {
                            Text("总场次")
                                .font(.caption)
                                .foregroundColor(.gray)
                            Text("\(totalGames)")
                                .font(.title2)
                                .fontWeight(.bold)
                                .foregroundColor(.orange)
                        }
                        
                        VStack {
                            Text("机械臂")
                                .font(.caption)
                                .foregroundColor(.gray)
                            Text("\(robotScore)")
                                .font(.title2)
                                .fontWeight(.bold)
                                .foregroundColor(.red)
                        }
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(12)
                }
                
                // 控制按钮
                VStack(spacing: 15) {
                    // 摄像头控制
                    Button(action: {
                        if showingCamera {
                            cameraManager.stopSession()
                            showingCamera = false
                        } else {
                            showingCamera = true
                            DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
                                cameraManager.startSession()
                            }
                        }
                    }) {
                        HStack {
                            Image(systemName: showingCamera ? "camera.fill" : "camera")
                            Text(showingCamera ? "关闭摄像头" : "启动摄像头")
                        }
                        .foregroundColor(.white)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(showingCamera ? Color.red : Color.blue)
                        .cornerRadius(12)
                    }
                    
                    // 游戏控制
                    Button(action: {
                        isGameActive.toggle()
                        if isGameActive {
                            startGame()
                        } else {
                            stopGame()
                        }
                    }) {
                        HStack {
                            Image(systemName: isGameActive ? "stop.fill" : "play.fill")
                            Text(isGameActive ? "停止游戏" : "开始游戏")
                        }
                        .foregroundColor(.white)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(isGameActive ? Color.red : Color.green)
                        .cornerRadius(12)
                    }
                    
                    // 手动测试按钮
                    VStack(spacing: 10) {
                        Text("手动测试手势")
                            .font(.headline)
                            .foregroundColor(.primary)
                        
                        HStack(spacing: 15) {
                            // 石头按钮
                            Button(action: {
                                print("🖐️ 石头按钮被点击")
                                print("🔗 按钮点击时连接状态: \(handController.isConnected)")
                                print("📡 按钮点击时状态信息: \(handController.connectionStatus)")
                                testManualGesture("石头")
                            }) {
                                VStack(spacing: 5) {
                                    Image(systemName: "hand.raised.fill")
                                        .font(.title2)
                                    Text("石头")
                                        .font(.caption)
                                }
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 12)
                                .background(Color.orange)
                                .cornerRadius(10)
                            }
                            
                            // 剪刀按钮
                            Button(action: {
                                print("✂️ 剪刀按钮被点击")
                                print("🔗 按钮点击时连接状态: \(handController.isConnected)")
                                print("📡 按钮点击时状态信息: \(handController.connectionStatus)")
                                testManualGesture("剪刀")
                            }) {
                                VStack(spacing: 5) {
                                    Image(systemName: "scissors")
                                        .font(.title2)
                                    Text("剪刀")
                                        .font(.caption)
                                }
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 12)
                                .background(Color.purple)
                                .cornerRadius(10)
                            }
                            
                            // 布按钮
                            Button(action: {
                                print("🖐️ 布按钮被点击")
                                print("🔗 按钮点击时连接状态: \(handController.isConnected)")
                                print("📡 按钮点击时状态信息: \(handController.connectionStatus)")
                                testManualGesture("布")
                            }) {
                                VStack(spacing: 5) {
                                    Image(systemName: "hand.raised")
                                        .font(.title2)
                                    Text("布")
                                        .font(.caption)
                                }
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 12)
                                .background(Color.blue)
                                .cornerRadius(10)
                            }
                        }
                        
                        // 重置按钮
                        Button(action: {
                            handController.sendResetCommand()
                            currentGesture = "等待识别..."
                            gameResult = ""
                        }) {
                            HStack {
                                Image(systemName: "arrow.clockwise")
                                Text("重置机械臂")
                            }
                            .foregroundColor(.white)
                            .padding(.vertical, 8)
                            .frame(maxWidth: .infinity)
                            .background(Color.gray)
                            .cornerRadius(8)
                        }
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(12)
                    
                    // 连接状态
                    HStack {
                        Circle()
                            .fill(handController.isConnected ? Color.green : Color.red)
                            .frame(width: 12, height: 12)
                        Text(handController.connectionStatus)
                            .font(.caption)
                        Spacer()
                        Button(action: {
                            handController.testConnection()
                        }) {
                            Text("重新连接")
                                .foregroundColor(.white)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 6)
                                .background(Color.blue)
                                .cornerRadius(6)
                        }
                        
                        Button(action: {
                            handController.simpleNetworkTest()
                        }) {
                            Text("网络测试")
                                .foregroundColor(.white)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 6)
                                .background(Color.orange)
                                .cornerRadius(6)
                        }
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(8)
                }
                
                Spacer()
            }
            .padding()
            .navigationTitle("石头剪刀布")
            .navigationBarTitleDisplayMode(.large)
            .onAppear {
                setupCameraManager()
                handController.testConnection()
            }
        }
    }
    
    private func setupCameraManager() {
        print("🔧 设置摄像头管理器...")
        cameraManager.setupDelegate { gesture, conf in
            print("🤚 收到手势识别结果: \(gesture), 置信度: \(conf)")
            DispatchQueue.main.async {
                self.processGestureRecognition(gesture: gesture, confidence: conf)
            }
        }
        print("✅ 摄像头管理器设置完成")
    }
    
    private func processGestureRecognition(gesture: String, confidence: Float) {
        print("🤚 处理手势识别: \(gesture), 置信度: \(confidence)")
        
        self.confidence = confidence
        self.isProcessing = false
        
        // 只处理高置信度的识别结果
        if confidence < 0.3 {
            print("🤚 置信度太低，忽略识别结果")
            if currentGesture != "等待识别..." {
                currentGesture = "等待识别..."
                gestureStabilityCount = 0
            }
            return
        }
        
        // 检查手势稳定性
        if gesture == lastValidGesture {
            gestureStabilityCount += 1
            print("🤚 手势稳定: \(gesture), 稳定性计数: \(gestureStabilityCount)")
        } else {
            gestureStabilityCount = 1
            lastValidGesture = gesture
            print("🤚 新手势: \(gesture), 重置稳定性计数")
        }
        
        // 当手势稳定2次以上就认为是有效识别
        if gestureStabilityCount >= 2 {
            print("🤚 手势识别有效: \(gesture)")
            currentGesture = gesture
            
            if isGameActive {
                gestureCount += 1
                print("🎮 游戏进行中，执行游戏逻辑")
                playGame(userGesture: gesture)
            } else {
                print("🎮 游戏未开始，只显示手势")
            }
        }
    }
    
    private func startGame() {
        gameResult = ""
        currentGesture = "等待识别..."
        gestureCount = 0
        gestureStabilityCount = 0
        lastValidGesture = ""
    }
    
    private func stopGame() {
        gameResult = ""
        currentGesture = "游戏已停止"
        gestureStabilityCount = 0
    }
    
    private func playGame(userGesture: String) {
        // 确保机械臂总是获胜
        let robotGesture = getWinningGesture(for: userGesture)
        let result = determineWinner(user: userGesture, robot: robotGesture)
        
        // 更新统计
        totalGames += 1
        robotScore += 1
        
        DispatchQueue.main.async {
            self.gameResult = result
            self.executeRobotGesture(robotGesture)
        }
    }
    
    private func getWinningGesture(for userGesture: String) -> String {
        switch userGesture {
        case "石头":
            return "布" // 布包石头
        case "剪刀":
            return "石头" // 石头砸剪刀
        case "布":
            return "剪刀" // 剪刀剪布
        default:
            return "石头"
        }
    }
    
    private func determineWinner(user: String, robot: String) -> String {
        return "你出\(user)，机械臂出\(robot)，机械臂获胜！"
    }
    
    private func executeRobotGesture(_ gesture: String) {
        print("🤖 执行机械臂手势: \(gesture)")
        print("🔗 执行前连接状态: \(handController.isConnected)")
        
        // 将中文手势名称转换为英文
        let englishGesture: String
        switch gesture {
        case "石头":
            englishGesture = "ROCK"
            print("🤖 转换: 石头 -> ROCK")
        case "剪刀":
            englishGesture = "SCISSORS"
            print("🤖 转换: 剪刀 -> SCISSORS")
        case "布":
            englishGesture = "PAPER"
            print("🤖 转换: 布 -> PAPER")
        default:
            englishGesture = "ROCK"
            print("🤖 转换: 默认 -> ROCK")
        }
        
        print("🤖 发送命令: \(englishGesture)")
        handController.sendRPSGesture(gesture: englishGesture)
        print("🤖 命令已发送，等待响应...")
    }
    
    // 手动测试手势
    private func testManualGesture(_ gesture: String) {
        print("🎮 手动测试手势: \(gesture)")
        print("🔗 当前连接状态: \(handController.isConnected)")
        print("📡 连接状态信息: \(handController.connectionStatus)")
        
        // 更新当前手势显示
        currentGesture = gesture
        
        // 如果游戏正在进行，执行游戏逻辑
        if isGameActive {
            print("🎮 游戏进行中，执行游戏逻辑")
            playGame(userGesture: gesture)
        } else {
            // 如果游戏未开始，只执行机械臂手势
            let robotGesture = getWinningGesture(for: gesture)
            let result = "你出\(gesture)，机械臂出\(robotGesture)，机械臂获胜！"
            
            print("🎮 游戏未开始，机械臂手势: \(robotGesture)")
            
            DispatchQueue.main.async {
                self.gameResult = result
                self.executeRobotGesture(robotGesture)
            }
        }
    }
    
    // 直接HTTP测试
    private func sendDirectHTTPTest(gesture: String) {
        guard let url = URL(string: "http://192.168.1.26:8081/rps") else {
            print("❌ 无效的测试URL")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let parameters = ["gesture": gesture == "石头" ? "ROCK" : gesture == "剪刀" ? "SCISSORS" : "PAPER"]
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters)
            print("📤 直接HTTP测试请求体: \(parameters)")
        } catch {
            print("❌ 直接HTTP测试序列化失败: \(error)")
            return
        }
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    print("❌ 直接HTTP测试失败: \(error)")
                } else if let httpResponse = response as? HTTPURLResponse {
                    print("✅ 直接HTTP测试成功，状态码: \(httpResponse.statusCode)")
                    if let data = data, let responseString = String(data: data, encoding: .utf8) {
                        print("📡 直接HTTP测试响应: \(responseString)")
                    }
                } else {
                    print("⚠️ 直接HTTP测试: 无HTTP响应")
                }
            }
        }.resume()
        
        print("🚀 直接HTTP测试请求已发送")
    }
}

// MARK: - Gesture Camera Manager
class GestureCameraManager: NSObject, ObservableObject {
    private var gestureCallback: ((String, Float) -> Void)?
    var captureSession: AVCaptureSession?
    private var videoOutput: AVCaptureVideoDataOutput?
    private var handPoseRequest = VNDetectHumanHandPoseRequest()
    private var lastGestureTime: Date = Date()
    private let gestureCooldown: TimeInterval = 0.3 // 0.3秒冷却时间，提高识别频率
    
    override init() {
        super.init()
        setupHandPoseRequest()
    }
    
    func setupDelegate(callback: @escaping (String, Float) -> Void) {
        self.gestureCallback = callback
    }
    
    private func setupHandPoseRequest() {
        handPoseRequest.maximumHandCount = 1
    }
    
    func startSession() {
        print("📹 开始启动摄像头...")
        
        // 先停止现有会话
        if let session = captureSession, session.isRunning {
            session.stopRunning()
            print("📹 停止现有会话")
        }
        
        // 清理旧的输出
        if let output = videoOutput {
            output.setSampleBufferDelegate(nil, queue: nil)
            print("📹 清理旧输出")
        }
        
        guard let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .front) else {
            print("❌ 无法访问前置摄像头")
            return
        }
        
        do {
            let input = try AVCaptureDeviceInput(device: device)
            print("📹 创建摄像头输入成功")
            
            // 创建新的会话和输出
            captureSession = AVCaptureSession()
            videoOutput = AVCaptureVideoDataOutput()
            
            guard let session = captureSession, let output = videoOutput else {
                print("❌ 创建摄像头会话失败")
                return
            }
            
            session.sessionPreset = .high
            print("📹 设置会话预设为high")
            
            DispatchQueue.global(qos: .userInitiated).async {
                print("📹 在后台线程配置会话...")
                session.beginConfiguration()
                
                // 添加输入
                if session.canAddInput(input) {
                    session.addInput(input)
                    print("📹 添加摄像头输入成功")
                } else {
                    print("❌ 无法添加摄像头输入")
                }
                
                // 添加输出
                output.setSampleBufferDelegate(self, queue: DispatchQueue.global(qos: .userInteractive))
                if session.canAddOutput(output) {
                    session.addOutput(output)
                    print("📹 添加视频输出成功")
                } else {
                    print("❌ 无法添加视频输出")
                }
                
                session.commitConfiguration()
                print("📹 会话配置完成")
                
                // 在后台线程启动摄像头
                session.startRunning()
                print("✅ 手势识别摄像头已启动")
                
                // 通知主线程会话已启动
                DispatchQueue.main.async {
                    print("📹 摄像头会话状态: \(session.isRunning ? "运行中" : "未运行")")
                }
            }
        } catch {
            print("❌ 摄像头设置失败: \(error)")
        }
    }
    
    func stopSession() {
        if let session = captureSession, session.isRunning {
            session.stopRunning()
        }
        
        // 清理输出
        if let output = videoOutput {
            output.setSampleBufferDelegate(nil, queue: nil)
        }
    }
    
    // 发送手部关键点数据到Python服务器
    private func sendHandDataToServer(handPose: VNHumanHandPoseObservation) {
        do {
            let points = try handPose.recognizedPoints(.all)
            print("🤚 获取到手部关键点，数量: \(points.count)")
            
            var handData: [String: Any] = [:]
            
            for (key, point) in points {
                let pointData: [String: Any] = [
                    "x": point.location.x,
                    "y": point.location.y,
                    "confidence": point.confidence
                ]
                handData[String(describing: key)] = pointData
            }
            
            print("📋 准备发送的关键点: \(Array(handData.keys))")
            sendHandDataToPython(handData: handData)
            
        } catch {
            print("❌ 处理手部数据失败: \(error)")
        }
    }
    
    private func sendHandDataToPython(handData: [String: Any]) {
        guard let url = URL(string: "http://192.168.1.26:8081/analyze_hand") else { 
            print("❌ 无效的URL: http://192.168.1.26:8081/analyze_hand")
            return 
        }
        
        print("📤 准备发送手部数据到服务器...")
        print("📊 手部数据包含 \(handData.count) 个关键点")
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: handData)
            request.httpBody = jsonData
            print("📦 序列化数据成功，大小: \(jsonData.count) 字节")
            
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("❌ 发送手部数据失败: \(error)")
                    return
                }
                
                if let httpResponse = response as? HTTPURLResponse {
                    print("📡 HTTP响应状态码: \(httpResponse.statusCode)")
                }
                
                if let data = data {
                    print("📥 收到服务器响应，数据大小: \(data.count) 字节")
                    
                    // 打印原始响应数据用于调试
                    if let responseString = String(data: data, encoding: .utf8) {
                        print("📄 服务器响应内容: \(responseString)")
                    }
                    
                    do {
                        if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                            print("✅ 成功解析JSON响应")
                            print("📋 JSON内容: \(json)")
                            
                            // 分别处理gesture和confidence字段
                            var gesture: String?
                            var confidence: Float?
                            
                            // 处理gesture字段
                            if let gestureValue = json["gesture"] {
                                if let gestureString = gestureValue as? String {
                                    gesture = gestureString
                                    print("✅ gesture字段解析成功: \(gestureString)")
                                } else {
                                    print("❌ gesture字段类型转换失败，类型: \(type(of: gestureValue)), 值: \(gestureValue)")
                                }
                            } else {
                                print("❌ 响应中缺少gesture字段")
                            }
                            
                            // 处理confidence字段
                            if let confidenceValue = json["confidence"] {
                                if let confidenceNumber = confidenceValue as? NSNumber {
                                    confidence = confidenceNumber.floatValue
                                    print("✅ confidence字段解析成功: \(confidenceNumber.floatValue)")
                                } else if let confidenceFloat = confidenceValue as? Float {
                                    confidence = confidenceFloat
                                    print("✅ confidence字段解析成功: \(confidenceFloat)")
                                } else {
                                    print("❌ confidence字段类型转换失败，类型: \(type(of: confidenceValue)), 值: \(confidenceValue)")
                                }
                            } else {
                                print("❌ 响应中缺少confidence字段")
                            }
                            
                            // 如果两个字段都解析成功，调用回调函数
                            if let finalGesture = gesture, let finalConfidence = confidence {
                                print("🎯 识别到手势: \(finalGesture), 置信度: \(finalConfidence)")
                                
                                DispatchQueue.main.async {
                                    print("🔄 调用手势回调函数")
                                    self.gestureCallback?(finalGesture, finalConfidence)
                                }
                            } else {
                                print("⚠️ 无法完整解析手势数据")
                            }
                        } else {
                            print("❌ 无法将响应解析为JSON字典")
                        }
                    } catch {
                        print("❌ 解析响应失败: \(error)")
                        if let responseString = String(data: data, encoding: .utf8) {
                            print("🔍 原始响应字符串: \(responseString)")
                        }
                    }
                } else {
                    print("⚠️ 服务器响应中没有数据")
                }
            }.resume()
            
        } catch {
            print("❌ 序列化手部数据失败: \(error)")
        }
    }
}

// MARK: - AVCaptureVideoDataOutputSampleBufferDelegate
extension GestureCameraManager: AVCaptureVideoDataOutputSampleBufferDelegate {
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        let now = Date()
        guard now.timeIntervalSince(lastGestureTime) >= gestureCooldown else { 
            print("⏰ 手势冷却中，跳过处理")
            return 
        }
        
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { 
            print("❌ 无法获取像素缓冲区")
            return 
        }
        
        let handler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, orientation: .up, options: [:])
        
        do {
            try handler.perform([handPoseRequest])
            
            guard let observation = handPoseRequest.results?.first else {
                print("🤚 未检测到手部")
                gestureCallback?("等待识别...", 0.0)
                return
            }
            
            print("✅ 检测到手部，准备发送数据到服务器")
            sendHandDataToServer(handPose: observation)
            lastGestureTime = Date()
            
        } catch {
            print("❌ 手势识别失败: \(error)")
        }
    }
}

// MARK: - Gesture Camera Preview View
struct GestureCameraPreviewView: UIViewRepresentable {
    let cameraManager: GestureCameraManager
    
    func makeUIView(context: Context) -> UIView {
        let view = UIView()
        view.backgroundColor = .black
        
        let previewLayer = AVCaptureVideoPreviewLayer()
        previewLayer.videoGravity = AVLayerVideoGravity.resizeAspectFill
        view.layer.addSublayer(previewLayer)
        
        // 设置会话
        if let session = cameraManager.captureSession {
            previewLayer.session = session
            print("✅ 预览层已设置会话")
        } else {
            print("⚠️ 预览层未找到会话")
        }
        
        // 添加手势识别覆盖层
        let overlayView = UIView()
        overlayView.backgroundColor = UIColor.clear
        view.addSubview(overlayView)
        
        // 添加调试信息
        print("📹 预览层创建完成")
        
        return view
    }
    
    func updateUIView(_ uiView: UIView, context: Context) {
        if let previewLayer = uiView.layer.sublayers?.first as? AVCaptureVideoPreviewLayer {
            DispatchQueue.main.async {
                previewLayer.frame = uiView.bounds
                print("📹 更新预览层frame: \(uiView.bounds)")
                
                if let overlayView = uiView.subviews.first {
                    overlayView.frame = uiView.bounds
                }
            }
        }
        
        // 确保预览层有会话
        if let previewLayer = uiView.layer.sublayers?.first as? AVCaptureVideoPreviewLayer {
            if previewLayer.session == nil, let session = cameraManager.captureSession {
                DispatchQueue.main.async {
                    previewLayer.session = session
                    print("✅ 预览层会话已更新")
                }
            }
        }
    }
}

#Preview {
    SimpleGestureRecognitionView()
}
