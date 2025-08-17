//
//  ContentView.swift
//  hand
//
//  Created by pluto guo on 8/16/25.
//

import SwiftUI

struct ContentView: View {
    @StateObject private var handController = HandController()
    @State private var selectedGesture = "无"
    @State private var servoValues = [0, 0, 0, 0, 0, 90] // 6个舵机的角度值（5个手指+手腕）
    
    // 预定义的手势（适配您的Arduino代码）
    let gestures = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
        "WAVE", "CLAP", "OK"
    ]
    
    var body: some View {
        NavigationView {
            ScrollView {
                            VStack(spacing: 20) {
                // 游戏选择区域
                VStack(spacing: 15) {
                    Text("游戏选择")
                        .font(.headline)
                        .frame(maxWidth: .infinity, alignment: .leading)
                    
                    // 石头剪刀布游戏
                    NavigationLink(destination: SimpleGestureRecognitionView()) {
                        HStack {
                            Image(systemName: "hand.raised.fill")
                                .font(.title2)
                            Text("✂️ 石头剪刀布")
                                .font(.headline)
                            Spacer()
                            Image(systemName: "chevron.right")
                                .foregroundColor(.gray)
                        }
                        .foregroundColor(.white)
                        .padding()
                        .background(Color.green)
                        .cornerRadius(12)
                    }
                    
                    // 摄像头手势识别游戏
                    NavigationLink(destination: SimpleCameraView()) {
                        HStack {
                            Image(systemName: "camera.fill")
                                .font(.title2)
                            Text("📷 AI手势识别")
                                .font(.headline)
                            Spacer()
                            Image(systemName: "chevron.right")
                                .foregroundColor(.gray)
                        }
                        .foregroundColor(.white)
                        .padding()
                        .background(Color.blue)
                        .cornerRadius(12)
                    }
                }
                
                // 连接状态和设置
                connectionSection
                
                // 手势选择区域
                gestureSelectionSection
                
                // 舵机控制区域
                servoControlSection
                
                // 快速动作按钮
                quickActionSection
                
                // 状态显示
                statusSection
                }
                .padding()
            }
        }
        .navigationTitle("机械手控制器")
        .navigationBarTitleDisplayMode(.large)
                    .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        handController.testConnection()
                    }) {
                        Image(systemName: "wifi")
                    }
                }
            }
        .onAppear {
            // 应用启动时自动连接到服务器
            handController.testConnection()
        }
    }
    
    // 连接状态区域
    private var connectionSection: some View {
        VStack(spacing: 10) {
            HStack {
                Circle()
                    .fill(handController.isConnected ? Color.green : Color.red)
                    .frame(width: 12, height: 12)
                Text(handController.connectionStatus)
                    .font(.headline)
                Spacer()
                Button(action: {
                    if handController.isConnected {
                        handController.disconnect()
                    } else {
                        handController.testConnection()
                    }
                }) {
                    Text(handController.isConnected ? "断开" : "连接")
                        .foregroundColor(.white)
                        .padding(.horizontal, 20)
                        .padding(.vertical, 8)
                        .background(handController.isConnected ? Color.red : Color.blue)
                        .cornerRadius(8)
                }
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    // 手势选择区域
    private var gestureSelectionSection: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("手势控制")
                .font(.headline)
            
            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 3), spacing: 10) {
                ForEach(gestures, id: \.self) { gesture in
                    Button(action: {
                        selectedGesture = gesture
                        executeGesture(gesture)
                    }) {
                        Text(gesture)
                            .foregroundColor(selectedGesture == gesture ? .white : .primary)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 12)
                            .background(selectedGesture == gesture ? Color.blue : Color(.systemGray5))
                            .cornerRadius(8)
                    }
                }
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    // 舵机控制区域
    private var servoControlSection: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("舵机控制")
                .font(.headline)
            
            ForEach(0..<6, id: \.self) { index in
                VStack(alignment: .leading, spacing: 5) {
                    HStack {
                        Text(getServoName(index))
                            .font(.subheadline)
                        Spacer()
                        Text("\(servoValues[index])°")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    
                    HStack {
                        Button("-") {
                            if servoValues[index] > 0 {
                                servoValues[index] -= 10
                                handController.sendServoCommand(servoIndex: index, angle: servoValues[index])
                            }
                        }
                        .frame(width: 40, height: 30)
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(6)
                        
                        Slider(value: Binding(
                            get: { Double(servoValues[index]) },
                            set: { newValue in
                                servoValues[index] = Int(newValue)
                                handController.sendServoCommand(servoIndex: index, angle: servoValues[index])
                            }
                        ), in: 0...180, step: 1)
                        
                        Button("+") {
                            if servoValues[index] < 180 {
                                servoValues[index] += 10
                                handController.sendServoCommand(servoIndex: index, angle: servoValues[index])
                            }
                        }
                        .frame(width: 40, height: 30)
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(6)
                    }
                }
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    // 快速动作区域
    private var quickActionSection: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("快速动作")
                .font(.headline)
            
            HStack(spacing: 10) {
                QuickActionButton(title: "复位", icon: "arrow.clockwise") {
                    handController.sendResetCommand()
                    resetAllServos()
                }
                
                QuickActionButton(title: "握拳", icon: "hand.raised.fill") {
                    executeGesture("0")
                }
                
                QuickActionButton(title: "张开", icon: "hand.raised") {
                    executeGesture("5")
                }
            }
            
            HStack(spacing: 10) {
                QuickActionButton(title: "指向", icon: "hand.point.up") {
                    executeGesture("1")
                }
                
                QuickActionButton(title: "OK", icon: "hand.thumbsup") {
                    executeGesture("OK")
                }
                
                QuickActionButton(title: "胜利", icon: "hand.raised") {
                    executeGesture("2")
                }
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    // 状态显示区域
    private var statusSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("状态信息")
                .font(.headline)
            
            VStack(alignment: .leading, spacing: 5) {
                StatusRow(label: "当前手势", value: selectedGesture)
                StatusRow(label: "连接状态", value: handController.isConnected ? "正常" : "断开")
                StatusRow(label: "小拇指", value: "\(servoValues[0])°")
                StatusRow(label: "无名指", value: "\(servoValues[1])°")
                StatusRow(label: "中指", value: "\(servoValues[2])°")
                StatusRow(label: "食指", value: "\(servoValues[3])°")
                StatusRow(label: "大拇指", value: "\(servoValues[4])°")
                StatusRow(label: "手腕", value: "\(servoValues[5])°")
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
    
    // MARK: - 功能函数
    
    private func executeGesture(_ gesture: String) {
        selectedGesture = gesture
        
        // 发送手势命令到电脑服务器
        handController.sendGestureCommand(gesture: gesture)
    }
    
    private func resetAllServos() {
        servoValues = [0, 0, 0, 0, 0, 90] // 手指张开，手腕中立
        handController.sendResetCommand()
    }
    
    // 获取舵机名称
    private func getServoName(_ index: Int) -> String {
        switch index {
        case 0: return "小拇指"
        case 1: return "无名指"
        case 2: return "中指"
        case 3: return "食指"
        case 4: return "大拇指"
        case 5: return "手腕"
        default: return "舵机\(index + 1)"
        }
    }
}

// MARK: - 辅助视图

struct QuickActionButton: View {
    let title: String
    let icon: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(spacing: 5) {
                Image(systemName: icon)
                    .font(.title2)
                Text(title)
                    .font(.caption)
            }
            .foregroundColor(.white)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 12)
            .background(Color.blue)
            .cornerRadius(8)
        }
    }
}

struct StatusRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
                .foregroundColor(.secondary)
            Spacer()
            Text(value)
                .fontWeight(.medium)
        }
    }
}

#Preview {
    ContentView()
}
