/*
 * 机械手控制器 - 修复版V2
 * 适用于Arduino Nano，使用串口通信
 * 
 * 硬件连接:
 * - 舵机1 (小拇指): 连接到引脚 3
 * - 舵机2 (无名指): 连接到引脚 4
 * - 舵机3 (中指): 连接到引脚 5
 * - 舵机4 (食指): 连接到引脚 6
 * - 舵机5 (大拇指): 连接到引脚 7
 * - 舵机6 (手腕): 连接到引脚 8
 * 
 * 功能:
 * - 数字手势 0-9
 * - 剪刀石头布手势
 * - 串口控制
 */

#include <Servo.h>

// 舵机配置
Servo myservo[6];

const int SERVO_COUNT = 6;
const int PINKY_INDEX = 0;      // 小拇指 - 接口3
const int RING_INDEX = 1;       // 无名指 - 接口4  
const int MIDDLE_INDEX = 2;     // 中指 - 接口5
const int INDEX_INDEX = 3;      // 食指 - 接口6
const int THUMB_INDEX = 4;      // 大拇指 - 接口7
const int WRIST_INDEX = 5;      // 手腕 - 接口8

// 舵机引脚
const int SERVO_PINS[6] = {3, 4, 5, 6, 7, 8};

// 角度配置
const int OPEN_ANGLE = 0;      // 手指完全张开角度
const int CLOSED_ANGLE = 180;  // 手指完全收拢角度
const int HALF_ANGLE = 90;     // 半开角度

// 当前角度记录
int currentAngle[SERVO_COUNT] = {0, 0, 0, 0, 0, 90};

// 目标角度记录
int targetAngle[SERVO_COUNT] = {0, 0, 0, 0, 0, 90};

// 动画速度
const int ANIMATION_SPEED = 15;

// 舵机连接状态
bool servoConnected[6] = {false, false, false, false, false, false};

// 检查舵机连接
bool checkServoConnection(int servoIndex) {
  if (servoIndex < 0 || servoIndex >= SERVO_COUNT) {
    return false;
  }
  
  // 尝试写入一个测试角度
  int testAngle = currentAngle[servoIndex];
  myservo[servoIndex].write(testAngle);
  delay(50);
  
  // 这里可以添加更复杂的连接检测逻辑
  // 目前简单返回true，假设舵机已连接
  return true;
}

// 初始化舵机
void initializeServos() {
  Serial.println("🔧 初始化舵机...");
  
  for (int i = 0; i < SERVO_COUNT; i++) {
    Serial.print("舵机 ");
    Serial.print(i);
    Serial.print(" (引脚 ");
    Serial.print(SERVO_PINS[i]);
    Serial.print("): ");
    
    // 尝试连接舵机
    if (myservo[i].attach(SERVO_PINS[i])) {
      servoConnected[i] = true;
      Serial.println("✅ 已连接");
    } else {
      servoConnected[i] = false;
      Serial.println("❌ 连接失败");
    }
    
    // 设置初始角度
    currentAngle[i] = (i < 5) ? OPEN_ANGLE : 90;
    targetAngle[i] = currentAngle[i];
    
    if (servoConnected[i]) {
      myservo[i].write(currentAngle[i]);
    }
    
    delay(100);
  }
  
  Serial.println("舵机初始化完成");
}

// 并行移动所有舵机到目标角度
void moveAllServosParallel() {
  bool allReached = false;
  int step = 2; // 每次移动的步长
  int maxSteps = 100; // 最大步数，防止无限循环
  int stepCount = 0;
  
  while (!allReached && stepCount < maxSteps) {
    allReached = true;
    stepCount++;
    
    for (int i = 0; i < SERVO_COUNT; i++) {
      if (servoConnected[i] && currentAngle[i] != targetAngle[i]) {
        allReached = false;
        
        // 计算移动方向
        if (currentAngle[i] < targetAngle[i]) {
          currentAngle[i] = min(currentAngle[i] + step, targetAngle[i]);
        } else {
          currentAngle[i] = max(currentAngle[i] - step, targetAngle[i]);
        }
        
        // 移动舵机
        myservo[i].write(currentAngle[i]);
      }
    }
    
    delay(ANIMATION_SPEED);
  }
  
  if (stepCount >= maxSteps) {
    Serial.println("⚠️ 舵机移动超时");
  }
}

// 设置单个舵机目标角度
void setServoTarget(int servoIndex, int angle) {
  if (servoIndex >= 0 && servoIndex < SERVO_COUNT) {
    targetAngle[servoIndex] = constrain(angle, 0, 180);
    
    if (!servoConnected[servoIndex]) {
      Serial.print("⚠️ 舵机 ");
      Serial.print(servoIndex);
      Serial.println(" 未连接");
    }
  }
}

// 设置手指状态
void setFinger(int fingerIndex, bool isOpen) {
  int angle = isOpen ? OPEN_ANGLE : CLOSED_ANGLE;
  setServoTarget(fingerIndex, angle);
}

// 设置所有手指状态
void setAllFingers(bool isOpen) {
  for (int i = 0; i < 5; i++) {
    setFinger(i, isOpen);
  }
}

// 执行移动
void executeMove() {
  Serial.println("🚀 执行舵机移动...");
  moveAllServosParallel();
  Serial.println("✅ 舵机移动完成");
}

// 数字手势 0-9
void makeNumberGesture(String number) {
  Serial.print("手势: ");
  Serial.println(number);
  
  if (number == "0") {
    // 握拳
    Serial.println("动作: 握拳");
    setAllFingers(false);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (number == "1") {
    // 指向手势
    Serial.println("动作: 指向");
    setFinger(PINKY_INDEX, false);
    setFinger(RING_INDEX, false);
    setFinger(MIDDLE_INDEX, false);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, false);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (number == "2") {
    // 胜利手势
    Serial.println("动作: 胜利");
    setFinger(PINKY_INDEX, false);
    setFinger(RING_INDEX, false);
    setFinger(MIDDLE_INDEX, true);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, false);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (number == "3") {
    // 三指手势
    Serial.println("动作: 三指");
    setFinger(PINKY_INDEX, false);
    setFinger(RING_INDEX, true);
    setFinger(MIDDLE_INDEX, true);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, false);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (number == "4") {
    // 四指手势
    Serial.println("动作: 四指");
    setFinger(PINKY_INDEX, true);
    setFinger(RING_INDEX, true);
    setFinger(MIDDLE_INDEX, true);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, false);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (number == "5") {
    // 张开手势
    Serial.println("动作: 张开");
    setAllFingers(true);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (number == "6") {
    // 六指手势
    Serial.println("动作: 六指");
    setFinger(PINKY_INDEX, true);
    setFinger(RING_INDEX, true);
    setFinger(MIDDLE_INDEX, true);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, true);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (number == "7") {
    // 七指手势
    Serial.println("动作: 七指");
    setFinger(PINKY_INDEX, true);
    setFinger(RING_INDEX, true);
    setFinger(MIDDLE_INDEX, true);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, true);
    setServoTarget(WRIST_INDEX, 60);
    executeMove();
  }
  else if (number == "8") {
    // 八指手势
    Serial.println("动作: 八指");
    setFinger(PINKY_INDEX, true);
    setFinger(RING_INDEX, true);
    setFinger(MIDDLE_INDEX, true);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, true);
    setServoTarget(WRIST_INDEX, 30);
    executeMove();
  }
  else if (number == "9") {
    // 九指手势
    Serial.println("动作: 九指");
    setFinger(PINKY_INDEX, true);
    setFinger(RING_INDEX, true);
    setFinger(MIDDLE_INDEX, true);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, true);
    setServoTarget(WRIST_INDEX, 0);
    executeMove();
  }
  else {
    Serial.println("❌ 无效的数字手势");
  }
}

// 剪刀石头布手势
void makeRPSGesture(String gesture) {
  Serial.print("RPS手势: ");
  Serial.println(gesture);
  
  if (gesture == "ROCK") {
    // 石头 - 握拳
    Serial.println("动作: 石头 (握拳)");
    setAllFingers(false);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (gesture == "PAPER") {
    // 布 - 张开手掌
    Serial.println("动作: 布 (张开)");
    setAllFingers(true);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (gesture == "SCISSORS") {
    // 剪刀 - 食指和中指张开，其他收拢
    Serial.println("动作: 剪刀 (食指中指)");
    setFinger(PINKY_INDEX, false);
    setFinger(RING_INDEX, false);
    setFinger(MIDDLE_INDEX, true);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, false);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else {
    Serial.println("❌ 无效的RPS手势");
  }
}

// 重置为张开状态
void resetToOpen() {
  Serial.println("🔄 重置为张开状态");
  setAllFingers(true);
  setServoTarget(WRIST_INDEX, 90);
  executeMove();
}

// 字符串比较函数
bool stringEquals(const String& str1, const String& str2) {
  return str1.equals(str2);
}

// 串口命令处理
void processSerialCommand(String command) {
  command.trim();
  
  if (command.length() == 0) return;
  
  Serial.print("📥 收到命令: ");
  Serial.println(command);
  
  // 检查是否是数字手势 0-9
  if (command.toInt() >= 0 && command.toInt() <= 9) {
    makeNumberGesture(command);
  }
  // 检查是否是剪刀石头布手势 - 使用字符串比较
  else if (stringEquals(command, "ROCK") || stringEquals(command, "PAPER") || stringEquals(command, "SCISSORS")) {
    Serial.println("🎯 识别为RPS手势");
    makeRPSGesture(command);
  }
  // 重置命令
  else if (stringEquals(command, "RESET")) {
    Serial.println("🔄 识别为重置命令");
    resetToOpen();
  }
  // 单个舵机控制命令
  else if (command.startsWith("SERVO:")) {
    // 格式: SERVO:index:angle
    int firstColon = command.indexOf(':');
    int secondColon = command.indexOf(':', firstColon + 1);
    
    if (firstColon != -1 && secondColon != -1) {
      int servoIndex = command.substring(firstColon + 1, secondColon).toInt();
      int angle = command.substring(secondColon + 1).toInt();
      
      Serial.print("🎯 舵机 ");
      Serial.print(servoIndex);
      Serial.print(" 到 ");
      Serial.print(angle);
      Serial.println(" 度");
      
      setServoTarget(servoIndex, angle);
      executeMove();
    } else {
      Serial.println("❌ 无效的舵机命令格式");
    }
  }
  // 未知命令
  else {
    Serial.print("❌ 未知命令: ");
    Serial.println(command);
    Serial.print("命令长度: ");
    Serial.println(command.length());
    Serial.print("命令内容: [");
    for (int i = 0; i < command.length(); i++) {
      Serial.print((int)command.charAt(i));
      Serial.print(" ");
    }
    Serial.println("]");
  }
}

// 设置函数
void setup() {
  Serial.begin(9600);
  
  Serial.println("🚀 机械手控制器启动...");
  Serial.println("🔧 初始化舵机...");
  
  // 初始化舵机
  initializeServos();
  
  delay(1000);
  
  Serial.println("✅ 机械手控制器就绪!");
  Serial.println("📋 支持命令:");
  Serial.println("- 数字手势: 0-9");
  Serial.println("- 剪刀石头布: ROCK, PAPER, SCISSORS");
  Serial.println("- 重置: RESET");
  Serial.println("- 单个舵机: SERVO:index:angle");
  Serial.println("⏳ 等待命令...");
}

// 主循环
void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    processSerialCommand(command);
  }
}
