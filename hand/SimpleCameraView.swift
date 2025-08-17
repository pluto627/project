//
//  SimpleCameraView.swift
//  hand
//
//  Created by pluto guo on 8/16/25.
//

import SwiftUI
import AVFoundation
import Vision

struct SimpleCameraView: View {
    @StateObject private var cameraManager = SimpleCameraManager()
    @StateObject private var handController = HandController()
    @State private var currentGesture: String = "等待识别..."
    @State private var gameResult: String = ""
    @State private var isGameActive = false
    @State private var showingCamera = false
    @State private var gestureCount = 0
    @State private var confidence: Float = 0.0
    @State private var lastValidGesture: String = ""
    @State private var gestureStabilityCount = 0
    @State private var isProcessing = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // 摄像头预览
                ZStack {
                    if showingCamera {
                        SimpleCameraPreviewView(cameraManager: cameraManager)
                            .frame(height: 300)
                            .cornerRadius(12)
                            .overlay(
                                RoundedRectangle(cornerRadius: 12)
                                    .stroke(Color.blue, lineWidth: 2)
                            )
                            .onAppear {
                                // 确保摄像头启动
                                DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                                    cameraManager.startSession()
                                }
                            }
                    } else {
                        RoundedRectangle(cornerRadius: 12)
                            .fill(Color.gray.opacity(0.3))
                            .frame(height: 300)
                            .overlay(
                                VStack {
                                    Image(systemName: "camera.fill")
                                        .font(.system(size: 50))
                                        .foregroundColor(.gray)
                                    Text("点击启动摄像头")
                                        .foregroundColor(.gray)
                                }
                            )
                    }
                    
                    // 添加实时状态指示器
                    if showingCamera {
                        VStack {
                            HStack {
                                Circle()
                                    .fill(Color.red)
                                    .frame(width: 8, height: 8)
                                Text("实时预览")
                                    .font(.caption)
                                    .foregroundColor(.white)
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(Color.black.opacity(0.6))
                                    .cornerRadius(4)
                                Spacer()
                            }
                            Spacer()
                        }
                        .padding(8)
                    }
                }
                
                // 手势识别结果
                VStack(spacing: 10) {
                    Text("识别到的手势")
                        .font(.headline)
                    Text(currentGesture)
                        .font(.title2)
                        .foregroundColor(.blue)
                        .padding()
                        .background(Color.blue.opacity(0.1))
                        .cornerRadius(8)
                    
                    // 处理状态
                    HStack {
                        if isProcessing {
                            ProgressView()
                                .scaleEffect(0.8)
                            Text("AI分析中...")
                                .font(.caption)
                                .foregroundColor(.orange)
                        } else {
                            Text("置信度: \(Int(confidence * 100))%")
                                .font(.caption)
                                .foregroundColor(.orange)
                        }
                        Spacer()
                        if gestureStabilityCount > 0 {
                            Text("稳定性: \(gestureStabilityCount)")
                                .font(.caption)
                                .foregroundColor(.green)
                        }
                    }
                    
                    if isGameActive {
                        Text("游戏进行中 - 识别次数: \(gestureCount)")
                            .font(.caption)
                            .foregroundColor(.green)
                    }
                }
                
                // 游戏结果
                if !gameResult.isEmpty {
                    VStack(spacing: 10) {
                        Text("游戏结果")
                            .font(.headline)
                        Text(gameResult)
                            .font(.title2)
                            .foregroundColor(.green)
                            .padding()
                            .background(Color.green.opacity(0.1))
                            .cornerRadius(8)
                    }
                }
                
                // 控制按钮
                VStack(spacing: 15) {
                    Button(action: {
                        if showingCamera {
                            cameraManager.stopSession()
                            showingCamera = false
                        } else {
                            showingCamera = true
                            // 延迟启动摄像头，确保UI更新完成
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
                        .background(showingCamera ? Color.red : Color.blue)
                        .cornerRadius(8)
                    }
                    
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
                        .background(isGameActive ? Color.red : Color.green)
                        .cornerRadius(8)
                    }
                    
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
                                .padding(.horizontal, 10)
                                .padding(.vertical, 5)
                                .background(Color.blue)
                                .cornerRadius(5)
                        }
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(8)
                }
                
                Spacer()
            }
            .padding()
            .navigationTitle("AI手势识别")
            .onAppear {
                cameraManager.setupDelegate { gesture, conf in
                    DispatchQueue.main.async {
                        self.processGestureRecognition(gesture: gesture, confidence: conf)
                    }
                }
                handController.testConnection()
            }
        }
    }
    
    private func processGestureRecognition(gesture: String, confidence: Float) {
        self.confidence = confidence
        self.isProcessing = false
        
        // 只处理高置信度的识别结果
        if confidence < 0.3 {
            if currentGesture != "等待识别..." {
                currentGesture = "等待识别..."
                gestureStabilityCount = 0
            }
            return
        }
        
        // 检查手势稳定性
        if gesture == lastValidGesture {
            gestureStabilityCount += 1
        } else {
            gestureStabilityCount = 1
            lastValidGesture = gesture
        }
        
        // 当手势稳定1次以上就认为是有效识别
        if gestureStabilityCount >= 1 {
            currentGesture = gesture
            
            if isGameActive {
                gestureCount += 1
                playGame(userGesture: gesture)
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
        let computerGesture = getWinningGesture(for: userGesture)
        let result = determineWinner(user: userGesture, computer: computerGesture)
        
        DispatchQueue.main.async {
            self.gameResult = result
            self.executeComputerGesture(computerGesture)
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
    
    private func determineWinner(user: String, computer: String) -> String {
        return "你出\(user)，机械手出\(computer)，机械手获胜！"
    }
    
    private func executeComputerGesture(_ gesture: String) {
        switch gesture {
        case "石头":
            handController.sendGestureCommand(gesture: "0") // 握拳
        case "剪刀":
            handController.sendGestureCommand(gesture: "2") // 胜利手势
        case "布":
            handController.sendGestureCommand(gesture: "5") // 张开
        default:
            handController.sendGestureCommand(gesture: "5")
        }
    }
}

// MARK: - Simple Camera Manager
class SimpleCameraManager: NSObject, ObservableObject {
    private var gestureCallback: ((String, Float) -> Void)?
    var captureSession: AVCaptureSession?
    private var videoOutput: AVCaptureVideoDataOutput?
    private var handPoseRequest = VNDetectHumanHandPoseRequest()
    private var lastGestureTime: Date = Date()
    private let gestureCooldown: TimeInterval = 1.0 // 1秒冷却时间
    
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
        // 先停止现有会话
        if let session = captureSession, session.isRunning {
            session.stopRunning()
        }
        
        // 清理旧的输出
        if let output = videoOutput {
            output.setSampleBufferDelegate(nil, queue: nil)
        }
        
        guard let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .front) else {
            print("无法访问前置摄像头")
            return
        }
        
        do {
            let input = try AVCaptureDeviceInput(device: device)
            
            // 创建新的会话和输出
            captureSession = AVCaptureSession()
            videoOutput = AVCaptureVideoDataOutput()
            
            guard let session = captureSession, let output = videoOutput else {
                print("创建摄像头会话失败")
                return
            }
            
            session.sessionPreset = .high
            
            // 在后台线程配置会话
            DispatchQueue.global(qos: .userInitiated).async {
                session.beginConfiguration()
                
                // 添加输入
                if session.canAddInput(input) {
                    session.addInput(input)
                }
                
                // 添加输出
                output.setSampleBufferDelegate(self, queue: DispatchQueue.global(qos: .userInteractive))
                if session.canAddOutput(output) {
                    session.addOutput(output)
                }
                
                session.commitConfiguration()
                
                // 启动会话
                session.startRunning()
                print("✅ 摄像头会话已启动")
            }
        } catch {
            print("摄像头设置失败: \(error)")
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
            
            // 构建关键点数据
            var handData: [String: Any] = [:]
            
            // 遍历所有关键点
            for (key, point) in points {
                let pointData: [String: Any] = [
                    "x": point.location.x,
                    "y": point.location.y,
                    "confidence": point.confidence
                ]
                handData[String(describing: key)] = pointData
            }
            
            // 发送到Python服务器
            sendHandDataToPython(handData: handData)
            
        } catch {
            print("处理手部数据失败: \(error)")
        }
    }
    
    private func sendHandDataToPython(handData: [String: Any]) {
        guard let url = URL(string: "http://192.168.1.26:8081/analyze_hand") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: handData)
            request.httpBody = jsonData
            
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("发送手部数据失败: \(error)")
                    return
                }
                
                if let data = data {
                    do {
                        if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
                           let gesture = json["gesture"] as? String,
                           let confidence = json["confidence"] as? Float {
                            
                            DispatchQueue.main.async {
                                self.gestureCallback?(gesture, confidence)
                            }
                        }
                    } catch {
                        print("解析响应失败: \(error)")
                    }
                }
            }.resume()
            
        } catch {
            print("序列化手部数据失败: \(error)")
        }
    }
}

// MARK: - AVCaptureVideoDataOutputSampleBufferDelegate
extension SimpleCameraManager: AVCaptureVideoDataOutputSampleBufferDelegate {
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        let now = Date()
        guard now.timeIntervalSince(lastGestureTime) >= gestureCooldown else { return }
        
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        
        let handler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, orientation: .up, options: [:])
        
        do {
            try handler.perform([handPoseRequest])
            
            guard let observation = handPoseRequest.results?.first else {
                gestureCallback?("等待识别...", 0.0)
                return
            }
            
            // 发送手部数据到Python服务器进行分析
            sendHandDataToServer(handPose: observation)
            lastGestureTime = Date()
            
        } catch {
            print("手势识别失败: \(error)")
        }
    }
}

// MARK: - Simple Camera Preview View
struct SimpleCameraPreviewView: UIViewRepresentable {
    let cameraManager: SimpleCameraManager
    
    func makeUIView(context: Context) -> UIView {
        let view = UIView()
        view.backgroundColor = .black
        
        // 创建预览层
        let previewLayer = AVCaptureVideoPreviewLayer()
        previewLayer.videoGravity = AVLayerVideoGravity.resizeAspectFill
        previewLayer.frame = view.bounds
        view.layer.addSublayer(previewLayer)
        
        // 设置会话
        if let session = cameraManager.captureSession {
            previewLayer.session = session
        }
        
        // 添加手势识别覆盖层
        let overlayView = UIView()
        overlayView.backgroundColor = UIColor.clear
        overlayView.frame = view.bounds
        view.addSubview(overlayView)
        
        return view
    }
    
    func updateUIView(_ uiView: UIView, context: Context) {
        // 更新预览层大小
        if let previewLayer = uiView.layer.sublayers?.first as? AVCaptureVideoPreviewLayer {
            DispatchQueue.main.async {
                previewLayer.frame = uiView.bounds
                
                // 更新覆盖层大小
                if let overlayView = uiView.subviews.first {
                    overlayView.frame = uiView.bounds
                }
            }
        }
        
        // 确保会话已设置
        if let previewLayer = uiView.layer.sublayers?.first as? AVCaptureVideoPreviewLayer,
           previewLayer.session == nil,
           let session = cameraManager.captureSession {
            DispatchQueue.main.async {
                previewLayer.session = session
            }
        }
    }
}

#Preview {
    SimpleCameraView()
}
