#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define BEEP_PIN 6

MFRC522 rfid(SS_PIN, RST_PIN);

// Tag UIDs - replace with your actual tag UIDs
byte speedBreakerTag[4] = {0x43, 0x65, 0xC1, 0x27};
byte noisePollutionTag[4] = {0x43, 0x63, 0x6F, 0x14};

void setup() {
  Serial.begin(115200);
  SPI.begin();
  rfid.PCD_Init();
  
  pinMode(BEEP_PIN, OUTPUT);
  startupBeep();
  Serial.println("SYSTEM_READY");
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return;
  }

  String tagID = getTagUID();
  Serial.print("TAG_UID:");
  Serial.println(tagID);

  if (compareTag(tagID, speedBreakerTag)) {
    handleSpeedBreaker();
  } else if (compareTag(tagID, noisePollutionTag)) {
    handleNoisePollution();
  } else {
    Serial.println("UNKNOWN_TAG");
    errorBeep();
  }

  rfid.PICC_HaltA();
  delay(300);
}

String getTagUID() {
  String tagID = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    tagID += String(rfid.uid.uidByte[i] < 0x10 ? "0" : "");
    tagID += String(rfid.uid.uidByte[i], HEX);
  }
  tagID.toUpperCase();
  return tagID;
}

bool compareTag(String tag1, byte* tag2) {
  String tag2Str = "";
  for (byte i = 0; i < 4; i++) {
    tag2Str += String(tag2[i] < 0x10 ? "0" : "");
    tag2Str += String(tag2[i], HEX);
  }
  tag2Str.toUpperCase();
  return tag1 == tag2Str;
}

void handleSpeedBreaker() {
  Serial.println("ALERT_TYPE:SPEED_BREAKER");
  playThreeBeeps(800, 200, 100);
}

void handleNoisePollution() {
  Serial.println("ALERT_TYPE:NOISE_POLLUTION");
  playThreeBeeps(1000, 200, 50);
}

void startupBeep() {
  tone(BEEP_PIN, 1200, 200);
  delay(200);
  noTone(BEEP_PIN);
}

void errorBeep() {
  tone(BEEP_PIN, 1500, 100);
  delay(100);
  noTone(BEEP_PIN);
}

void playThreeBeeps(int freq, int duration, int gap) {
  for (int i = 0; i < 3; i++) {
    tone(BEEP_PIN, freq, duration);
    delay(duration + gap);
    noTone(BEEP_PIN);
  }
}