SM SwitchSM(SwitchIdle  );

#define PIN_SW 12

void ExecSwitchSM() {
    EXEC(SwitchSM);
}

void InitSwitch() {
  pinMode(PIN_SW, INPUT_PULLUP);
  wifi.print("!\n"); // request one update from wifi
  Serial.println("!");
}

State SwitchIdle() {
  if (digitalRead(PIN_SW) == LOW) {
    wifi.print("1\n"); // enable continuous updates from wifi
    Serial.println("1");
    SwitchSM.Set(SwitchActive);
  }
}

State SwitchActive() {
  if (digitalRead(PIN_SW) == HIGH) {
    wifi.print("0\n"); // disable updates from wifi
    Serial.println("0");
    SwitchSM.Set(SwitchIdle);
  }
}
