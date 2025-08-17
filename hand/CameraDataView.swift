//
//  CameraDataView.swift
//  hand
//
//  Created by pluto guo on 8/16/25.
//

import SwiftUI
import AVFoundation
import Vision

struct CameraDataView: View {
    @StateObject private var cameraManager = CameraDataManager()
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
                if showingCamera {
                    CameraDataPreviewView(cameraManager: cameraManager)
                        .frame(height: 300)
                        .cornerRadius(12)
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(Color.blue, lineWidth: 2)
                        )
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
                            cameraManager.startSession()
                            showingCamera = true
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
                    
                    // 测试按钮
                    VStack(spacing: 10) {
                        Text("测试机械臂控制")
                            .font(.headline)
                        
                        HStack(spacing: 10) {
                            Button("石头") {
                                handController.sendRPSGesture(gesture: "ROCK")
                            }
                            .foregroundColor(.white)
                            .padding()
                            .background(Color.red)
                            .cornerRadius(8)
                            
                            Button("剪刀") {
                                handController.sendRPSGesture(gesture: "SCISSORS")
                            }
                            .foregroundColor(.white)
                            .padding()
                            .background(Color.blue)
                            .cornerRadius(8)
                            
                            Button("布") {
                                handController.sendRPSGesture(gesture: "PAPER")
                            }
                            .foregroundColor(.white)
                            .padding()
                            .background(Color.green)
                            .cornerRadius(8)
                        }
                        
                        HStack(spacing: 10) {
                            Button("数字1") {
                                handController.sendGestureCommand(gesture: "1")
                            }
                            .foregroundColor(.white)
                            .padding()
                            .background(Color.orange)
                            .cornerRadius(8)
                            
                            Button("重置") {
                                handController.sendResetCommand()
                            }
                            .foregroundColor(.white)
                            .padding()
                            .background(Color.purple)
                            .cornerRadius(8)
                        }
                    }
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
        if confidence < 0.5 {
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
        
        // 只有当手势稳定2次以上才认为是有效识别
        if gestureStabilityCount >= 2 {
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
            handController.sendRPSGesture(gesture: "ROCK") // 石头
        case "剪刀":
            handController.sendRPSGesture(gesture: "SCISSORS") // 剪刀
        case "布":
            handController.sendRPSGesture(gesture: "PAPER") // 布
        default:
            handController.sendRPSGesture(gesture: "ROCK")
        }
    }
}

// MARK: - Camera Data Manager
class CameraDataManager: NSObject, ObservableObject {
    private var gestureCallback: ((String, Float) -> Void)?
    var captureSession: AVCaptureSession?
    private var videoOutput = AVCaptureVideoDataOutput()
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
        guard let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .front) else {
            print("无法访问前置摄像头")
            return
        }
        
        do {
            let input = try AVCaptureDeviceInput(device: device)
            captureSession = AVCaptureSession()
            captureSession?.sessionPreset = .high
            captureSession?.addInput(input)
            
            videoOutput.setSampleBufferDelegate(self, queue: DispatchQueue.global(qos: .userInteractive))
            captureSession?.addOutput(videoOutput)
            
            DispatchQueue.global(qos: .background).async {
                self.captureSession?.startRunning()
            }
        } catch {
            print("摄像头设置失败: \(error)")
        }
    }
    
    func stopSession() {
        captureSession?.stopRunning()
    }
    
    // 本地手势识别（简化版本）
    private func recognizeGestureLocally(handPose: VNHumanHandPoseObservation) {
        do {
            let points = try handPose.recognizedPoints(.all)
            
            // 简化的手势识别逻辑
            // 这里可以根据需要实现更复杂的手势识别算法
            let gesture = "石头" // 默认手势
            let confidence: Float = 0.8 // 默认置信度
            
            DispatchQueue.main.async {
                self.gestureCallback?(gesture, confidence)
            }
            
        } catch {
            print("处理手部数据失败: \(error)")
        }
    }
}

// MARK: - AVCaptureVideoDataOutputSampleBufferDelegate
extension CameraDataManager: AVCaptureVideoDataOutputSampleBufferDelegate {
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
            
            // 本地手势识别
            recognizeGestureLocally(handPose: observation)
            lastGestureTime = Date()
            
        } catch {
            print("手势识别失败: \(error)")
        }
    }
}

// MARK: - Camera Data Preview View
struct CameraDataPreviewView: UIViewRepresentable {
    let cameraManager: CameraDataManager
    
    func makeUIView(context: Context) -> UIView {
        let view = UIView()
        view.backgroundColor = .black
        
        if let session = cameraManager.captureSession {
            let previewLayer = AVCaptureVideoPreviewLayer(session: session)
            previewLayer.frame = view.bounds
            previewLayer.videoGravity = AVLayerVideoGravity.resizeAspectFill
            view.layer.addSublayer(previewLayer)
        }
        
        return view
    }
    
    func updateUIView(_ uiView: UIView, context: Context) {
        if let previewLayer = uiView.layer.sublayers?.first as? AVCaptureVideoPreviewLayer {
            previewLayer.frame = uiView.bounds
        }
    }
}

#Preview {
    CameraDataView()
}
