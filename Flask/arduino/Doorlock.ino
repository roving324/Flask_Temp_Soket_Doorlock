#include<LiquidCrystal_I2C_Hangul.h>
#include <Keypad.h>
#include <Servo.h>
// keypad
const byte ROWS = 4;  // 행(rows) 개수
const byte COLS = 4;  // 열(columns) 개수
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte rowPins[ROWS] = {46, 48, 50, 52}; // R1, R2, R3, R4 단자가 연결된 아두이노
byte colPins[COLS] = {44, 42, 40, 38}; // C1, C2, C3, C4 단자가 연결된 아두이노

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// servo
Servo myservo;
int pos = 0;

// LCD
LiquidCrystal_I2C_Hangul lcd(0x27,16,2);

// Variable
int count = 0;
String PW = "";
String CPW = "#9";
String APW = "";
String lcdpw = "";
String num = "";
bool bflag = false;
bool flag = false;

// LCD Print
void LPrint(int location,String msg = "",bool serial = false){
  lcd.setCursor(0,location);
  lcd.print("                ");
  lcd.setCursor(0,location);
  lcd.print(msg);
  if (serial){
    Serial3.println(msg);
    PW = "";
    lcdpw = "";
  }
}

// Change LCD Print
void CPWPrint(String msg, int location = 0){
  LPrint(location,msg,true);
  delay(1000);
  LPrint(0,"password : ",true);
  LPrint(1);
}

void setup() {
  Serial.begin(9600);
  Serial3.begin(9600);
  myservo.attach(9);
  pinMode(A0,OUTPUT);
  digitalWrite(A0,HIGH);
  pinMode(8,OUTPUT);
  digitalWrite(8,HIGH);
  lcd.init();
  lcd.backlight();
  LPrint(0,"password : ",true);
}

void loop() {
  while(Serial3.available()){
    num = Serial3.readString();
    PW += num;
    Serial.println(num);
    lcdpw += "*";
    LPrint(1,lcdpw);
  }
  while(Serial.available()){
    num = Serial.readString();
    if (APW.length() > 4){
      APW = "";
    }
    APW += num;
    if (APW.length() == 4){
      flag = true;
    }
  }
  char key = keypad.getKey();
  if (key){
    num = String(key);
    PW += num;
    Serial.println(num);
    lcdpw += "*";
    LPrint(1,lcdpw);
  }
  if (PW == CPW){
    LPrint(0,"Change PW + '*'",true);
    LPrint(1);
    while (true){
      char key = keypad.getKey();
      if (key){
        num = String(key);
        PW += String(key);
        Serial.println(num);
        LPrint(1,PW);
      }
      while(Serial3.available()){
        num = Serial3.readString();
        PW += num;
        Serial.println(num);
        LPrint(1,PW);
      }
      if (PW.length() > 5){
        CPWPrint("Change PW Fail!");
        break;
      }
      if (PW.length() == 5){
        if (PW.substring(4,5) != "*"){
          CPWPrint("Change PW Fail!");
          break;
        }
        // keypad use flag
        for (int i = 0; i < 4; i++){
          for (int j = 0; j < 4; j++){
            for (int k = 0; k < 4; k++){
              if (PW.substring(i,i+1) == String(keys[j][k])){
                LPrint(1,PW);
                bflag = true;
              }
            }
          }
          if (!bflag){
            break;
          }
          else if (i < 3){
            bflag = false;
          }
        }
        if (bflag){
          APW = PW.substring(0,4);
          bflag = false;
          CPWPrint("Success",1);
          break;
        }
        else{
          CPWPrint("Change PW Fail!");
          break;
        }
      }
    }
  }
  if (PW.length() > 3 && flag){
    flag = false;
    if (PW == APW){
      LPrint(0,"Success PW",true);
      LPrint(1,"open the door",true);
      for (pos = 0; pos <= 180; pos += 1) { 
        myservo.write(pos);
        delay(15);
      }
      delay(3000);
      LPrint(1,"close the door",true);
      for (pos = 180; pos >= 0; pos -= 1){
        myservo.write(pos);              
        delay(15);                       
      }
    }
    else{
      LPrint(1,"fail",true);
    }
    delay(1000);
    LPrint(0,"password : ",true);
    LPrint(1);
  }
}
