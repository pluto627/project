/*
 * 机械手控制器 - 简化版
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

// 并行移动所有舵机到目标角度
void moveAllServosParallel() {
  bool allReached = false;
  int step = 2; // 每次移动的步长
  
  while (!allReached) {
    allReached = true;
    
    for (int i = 0; i < SERVO_COUNT; i++) {
      if (currentAngle[i] != targetAngle[i]) {
        allReached = false;
        
        // 计算移动方向
        if (currentAngle[i] < targetAngle[i]) {
          currentAngle[i] = min(currentAngle[i] + step, targetAngle[i]);
        } else {
          currentAngle[i] = max(currentAngle[i] - step, targetAngle[i]);
        }
        
        // 同时移动舵机
        myservo[i].write(currentAngle[i]);
      }
    }
    
    delay(ANIMATION_SPEED);
  }
}

// 设置单个舵机目标角度
void setServoTarget(int servoIndex, int angle) {
  if (servoIndex >= 0 && servoIndex < SERVO_COUNT) {
    targetAngle[servoIndex] = constrain(angle, 0, 180);
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
  moveAllServosParallel();
}

// 数字手势 0-9
void makeNumberGesture(String number) {
  if (number == "0") {
    // 握拳
    Serial.println("手势: 0 (握拳)");
    setAllFingers(false);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (number == "1") {
    // 指向手势
    Serial.println("手势: 1 (指向)");
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
    Serial.println("手势: 2 (胜利)");
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
    Serial.println("手势: 3");
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
    Serial.println("手势: 4");
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
    Serial.println("手势: 5 (张开)");
    setAllFingers(true);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (number == "6") {
    // 六指手势
    Serial.println("手势: 6");
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
    Serial.println("手势: 7");
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
    Serial.println("手势: 8");
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
    Serial.println("手势: 9");
    setFinger(PINKY_INDEX, true);
    setFinger(RING_INDEX, true);
    setFinger(MIDDLE_INDEX, true);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, true);
    setServoTarget(WRIST_INDEX, 0);
    executeMove();
  }
}

// 剪刀石头布手势
void makeRPSGesture(String gesture) {
  if (gesture == "ROCK") {
    // 石头 - 握拳
    Serial.println("手势: 石头");
    setAllFingers(false);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (gesture == "PAPER") {
    // 布 - 张开手掌
    Serial.println("手势: 布");
    setAllFingers(true);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
  else if (gesture == "SCISSORS") {
    // 剪刀 - 食指和中指张开，其他收拢
    Serial.println("手势: 剪刀");
    setFinger(PINKY_INDEX, false);
    setFinger(RING_INDEX, false);
    setFinger(MIDDLE_INDEX, true);
    setFinger(INDEX_INDEX, true);
    setFinger(THUMB_INDEX, false);
    setServoTarget(WRIST_INDEX, 90);
    executeMove();
  }
}

// 重置为张开状态
void resetToOpen() {
  Serial.println("重置为张开状态");
  setAllFingers(true);
  setServoTarget(WRIST_INDEX, 90);
  executeMove();
}

// 机械手全部张开到最大
void openHandMax() {
  Serial.println("🖐️ 机械手全部张开到最大");
  
  // 所有手指都张开到最大角度 (0度)
  for (int i = 0; i < 5; i++) {
    setServoTarget(i, 0);  // 0度 = 完全张开
  }
  
  // 手腕保持中立位置
  setServoTarget(WRIST_INDEX, 90);
  
  // 执行移动
  executeMove();
  
  Serial.println("✅ 机械手已全部张开到最大");
}

// 机械手全部握拳
void closeHandMax() {
  Serial.println("👊 机械手全部握拳");
  
  // 所有手指都握拳到最大角度 (180度)
  for (int i = 0; i < 5; i++) {
    setServoTarget(i, 180);  // 180度 = 完全握拳
  }
  
  // 手腕保持中立位置
  setServoTarget(WRIST_INDEX, 90);
  
  // 执行移动
  executeMove();
  
  Serial.println("✅ 机械手已全部握拳");
}

// 串口命令处理
void processSerialCommand(String command) {
  command.trim();
  
  if (command.length() == 0) return;
  
  Serial.print("收到命令: ");
  Serial.println(command);
  
  // 检查是否是数字手势 0-9
  if (command.toInt() >= 0 && command.toInt() <= 9) {
    makeNumberGesture(command);
  }
  // 检查是否是剪刀石头布手势
  else if (command == "ROCK" || command == "PAPER" || command == "SCISSORS") {
    makeRPSGesture(command);
  }
  // 重置命令
  else if (command == "RESET") {
    resetToOpen();
  }
  // 机械手全部张开到最大
  else if (command == "OPENMAX") {
    openHandMax();
  }
  // 机械手全部握拳
  else if (command == "CLOSEMAX") {
    closeHandMax();
  }
  // 未知命令
  else {
    Serial.print("未知命令: ");
    Serial.println(command);
  }
}

// 设置函数
void setup() {
  Serial.begin(9600);
  
  // 初始化舵机
  myservo[PINKY_INDEX].attach(3);   // 小拇指 - 引脚3
  myservo[RING_INDEX].attach(4);    // 无名指 - 引脚4
  myservo[MIDDLE_INDEX].attach(5);  // 中指 - 引脚5
  myservo[INDEX_INDEX].attach(6);   // 食指 - 引脚6
  myservo[THUMB_INDEX].attach(7);   // 大拇指 - 引脚7
  myservo[WRIST_INDEX].attach(8);   // 手腕 - 引脚8
  
  // 初始化所有舵机到默认位置
  for (int i = 0; i < SERVO_COUNT; i++) {
    currentAngle[i] = (i < 5) ? OPEN_ANGLE : 90;
    targetAngle[i] = currentAngle[i];
    myservo[i].write(currentAngle[i]);
  }
  
  delay(1000);
  
  Serial.println("机械手控制器就绪!");
  Serial.println("支持命令:");
  Serial.println("- 数字手势: 0-9");
  Serial.println("- 剪刀石头布: ROCK, PAPER, SCISSORS");
  Serial.println("- 重置: RESET");
  Serial.println("- 全部张开: OPENMAX");
  Serial.println("- 全部握拳: CLOSEMAX");
  Serial.println("等待命令...");
}

// 主循环
void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    processSerialCommand(command);
  }
}
