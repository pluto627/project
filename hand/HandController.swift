//
//  HandController.swift
//  hand
//
//  Created by pluto guo on 8/16/25.
//

import Foundation
import Network

class HandController: ObservableObject {
    @Published var isConnected = false
    @Published var connectionStatus = "未连接"
    
    // 直接使用您的电脑服务器地址
    // 请确保您的iPhone和电脑在同一个WiFi网络下
    // 如果连接失败，请检查电脑的IP地址并更新下面的地址
    private var serverURL = "http://192.168.1.26:8081"
    
    func connect(to ipAddress: String, port: UInt16) {
        // 直接连接到服务器
        testConnection()
    }
    
    func disconnect() {
        isConnected = false
        connectionStatus = "已断开"
    }
    
    func sendServoCommand(servoIndex: Int, angle: Int) {
        guard isConnected else {
            print("❌ 未连接到机械手")
            return
        }
        
        // 发送HTTP请求到电脑服务器
        sendHTTPRequest(endpoint: "command", parameters: [
            "command": "SERVO:\(servoIndex):\(angle)"
        ])
    }
    
    func sendGestureCommand(gesture: String) {
        guard isConnected else {
            print("❌ 未连接到机械手")
            return
        }
        
        // 根据手势类型发送到不同的端点
        if let number = Int(gesture), number >= 0 && number <= 9 {
            // 数字手势 (0-9)
            sendHTTPRequest(endpoint: "number", parameters: [
                "number": gesture
            ])
        } else {
            // 其他手势，发送到command端点
            sendHTTPRequest(endpoint: "command", parameters: [
                "command": gesture
            ])
        }
    }
    
    func sendRPSGesture(gesture: String) {
        // 移除连接检查，直接发送请求
        print("🤖 发送RPS手势: \(gesture)")
        
        // 使用简化的HTTP请求
        sendSimpleHTTPRequest(endpoint: "rps", parameters: [
            "gesture": gesture
        ])
    }
    
    func sendResetCommand() {
        // 移除连接检查，直接发送请求
        print("🔄 发送重置命令")
        
        // 发送重置命令
        sendSimpleHTTPRequest(endpoint: "reset", parameters: [:])
    }
    
    // HTTP方式发送命令到电脑服务器
    func sendHTTPRequest(endpoint: String, parameters: [String: Any]) {
        guard let url = URL(string: "\(serverURL)/\(endpoint)") else {
            print("❌ 无效的URL: \(serverURL)/\(endpoint)")
            DispatchQueue.main.async {
                self.connectionStatus = "无效的URL"
            }
            return
        }
        
        print("🌐 发送HTTP请求到: \(url)")
        print("📦 请求参数: \(parameters)")
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.timeoutInterval = 10.0 // 设置10秒超时
        
        // 配置允许HTTP连接
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 10
        config.timeoutIntervalForResource = 20
        let session = URLSession(configuration: config)
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: parameters)
            request.httpBody = jsonData
            print("📤 请求体大小: \(jsonData.count) 字节")
        } catch {
            print("❌ 序列化参数失败: \(error)")
            DispatchQueue.main.async {
                self.connectionStatus = "序列化失败: \(error.localizedDescription)"
            }
            return
        }
        
        print("🚀 开始发送请求...")
        
        session.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    print("❌ HTTP请求失败: \(error)")
                    self.connectionStatus = "请求失败: \(error.localizedDescription)"
                    return
                }
                
                if let httpResponse = response as? HTTPURLResponse {
                    print("📡 HTTP状态码: \(httpResponse.statusCode)")
                    
                    if httpResponse.statusCode != 200 {
                        print("❌ HTTP错误状态码: \(httpResponse.statusCode)")
                        self.connectionStatus = "HTTP错误: \(httpResponse.statusCode)"
                        return
                    }
                }
                
                if let data = data {
                    if let responseString = String(data: data, encoding: .utf8) {
                        print("✅ HTTP响应: \(responseString)")
                        
                        // 尝试解析JSON响应
                        do {
                            if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                                if let success = json["success"] as? Bool {
                                    if success {
                                        self.connectionStatus = "命令发送成功"
                                        print("✅ 命令执行成功")
                                    } else {
                                        let message = json["message"] as? String ?? "未知错误"
                                        self.connectionStatus = "命令失败: \(message)"
                                        print("❌ 命令执行失败: \(message)")
                                    }
                                } else {
                                    self.connectionStatus = "命令发送成功"
                                    print("✅ 命令发送成功")
                                }
                            } else {
                                self.connectionStatus = "命令发送成功"
                                print("✅ 命令发送成功")
                            }
                        } catch {
                            print("⚠️ JSON解析失败: \(error)")
                            self.connectionStatus = "命令发送成功"
                        }
                    } else {
                        print("⚠️ 响应数据无法解码为字符串")
                        self.connectionStatus = "命令发送成功"
                    }
                } else {
                    print("⚠️ 没有响应数据")
                    self.connectionStatus = "命令发送成功"
                }
            }
        }.resume()
        
        print("📤 请求已发送，等待响应...")
    }
    
    // 测试连接
    func testConnection() {
        guard let url = URL(string: "\(serverURL)/status") else {
            print("❌ 无效的状态检查URL: \(serverURL)/status")
            connectionStatus = "无效的URL"
            return
        }
        
        print("🔗 测试连接到: \(url)")
        
        // 配置允许HTTP连接
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 10
        config.timeoutIntervalForResource = 20
        let session = URLSession(configuration: config)
        
        session.dataTask(with: url) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    print("❌ 连接测试失败: \(error)")
                    self.connectionStatus = "连接失败: \(error.localizedDescription)"
                    self.isConnected = false
                    return
                }
                
                if let httpResponse = response as? HTTPURLResponse {
                    print("📡 状态检查HTTP状态码: \(httpResponse.statusCode)")
                    
                    if httpResponse.statusCode != 200 {
                        print("❌ 状态检查HTTP错误: \(httpResponse.statusCode)")
                        self.connectionStatus = "HTTP错误: \(httpResponse.statusCode)"
                        self.isConnected = false
                        return
                    }
                }
                
                if let data = data, let responseString = String(data: data, encoding: .utf8) {
                    print("✅ 状态检查响应: \(responseString)")
                    
                    // 尝试解析JSON响应
                    do {
                        if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] {
                            if let status = json["status"] as? String, status == "running" {
                                let arduinoConnected = json["arduino_connected"] as? Bool ?? false
                                self.connectionStatus = "已连接到电脑服务器" + (arduinoConnected ? " (Arduino已连接)" : " (Arduino未连接)")
                                self.isConnected = true
                                print("✅ 连接测试成功，Arduino状态: \(arduinoConnected ? "已连接" : "未连接")")
                            } else {
                                self.connectionStatus = "服务器状态异常"
                                self.isConnected = false
                                print("❌ 服务器状态异常")
                            }
                        } else {
                            self.connectionStatus = "已连接到电脑服务器"
                            self.isConnected = true
                            print("✅ 连接测试成功")
                        }
                    } catch {
                        print("⚠️ 状态检查JSON解析失败: \(error)")
                        self.connectionStatus = "已连接到电脑服务器"
                        self.isConnected = true
                    }
                } else {
                    print("⚠️ 状态检查没有响应数据")
                    self.connectionStatus = "已连接到电脑服务器"
                    self.isConnected = true
                }
            }
        }.resume()
        
        print("�� 开始连接测试...")
    }
    
    // 简单网络测试
    func simpleNetworkTest() {
        print("🧪 开始简单网络测试...")
        
        // 测试1: 简单的GET请求
        guard let url = URL(string: "\(serverURL)/status") else {
            print("❌ 无效的测试URL")
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    print("❌ 简单网络测试失败: \(error)")
                    self.connectionStatus = "网络测试失败: \(error.localizedDescription)"
                } else if let httpResponse = response as? HTTPURLResponse {
                    print("✅ 简单网络测试成功，状态码: \(httpResponse.statusCode)")
                    self.connectionStatus = "网络测试成功 (状态码: \(httpResponse.statusCode))"
                } else {
                    print("⚠️ 简单网络测试: 无HTTP响应")
                    self.connectionStatus = "网络测试: 无HTTP响应"
                }
            }
        }
        
        task.resume()
        print("🚀 简单网络测试请求已发送")
    }
    
    // 简化的HTTP请求
    func sendSimpleHTTPRequest(endpoint: String, parameters: [String: Any]) {
        guard let url = URL(string: "\(serverURL)/\(endpoint)") else {
            print("❌ 无效的URL: \(serverURL)/\(endpoint)")
            return
        }
        
        print("🌐 发送简化HTTP请求到: \(url)")
        print("📦 请求参数: \(parameters)")
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.timeoutInterval = 5.0 // 缩短超时时间
        
        do {
            let jsonData = try JSONSerialization.data(withJSONObject: parameters)
            request.httpBody = jsonData
            print("📤 简化请求体大小: \(jsonData.count) 字节")
        } catch {
            print("❌ 简化请求序列化失败: \(error)")
            return
        }
        
        print("🚀 开始发送简化请求...")
        
        // 使用默认的URLSession
        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    print("❌ 简化HTTP请求失败: \(error)")
                    self.connectionStatus = "请求失败: \(error.localizedDescription)"
                    return
                }
                
                if let httpResponse = response as? HTTPURLResponse {
                    print("📡 简化HTTP状态码: \(httpResponse.statusCode)")
                    
                    if httpResponse.statusCode != 200 {
                        print("❌ 简化HTTP错误状态码: \(httpResponse.statusCode)")
                        self.connectionStatus = "HTTP错误: \(httpResponse.statusCode)"
                        return
                    }
                }
                
                if let data = data {
                    if let responseString = String(data: data, encoding: .utf8) {
                        print("✅ 简化HTTP响应: \(responseString)")
                        self.connectionStatus = "命令发送成功"
                    } else {
                        print("⚠️ 简化响应数据无法解码")
                        self.connectionStatus = "命令发送成功"
                    }
                } else {
                    print("⚠️ 简化请求没有响应数据")
                    self.connectionStatus = "命令发送成功"
                }
            }
        }.resume()
        
        print("📤 简化请求已发送，等待响应...")
    }
}
