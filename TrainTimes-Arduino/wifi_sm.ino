SM WiFiSM  (WiFiIdle    );

void ExecWifiSM() {
    EXEC(WiFiSM);
}

State WiFiIdle() {
  if (wifi.available() > 0) {
    WiFiSM.Set(WiFiStartReceive);
  }
}

State WiFiStartReceive() {
  char buf = wifi.read();
  if (buf == '{') {
    WiFiSM.Set(WiFiFoundStartChar);
  }
  if (wifi.available() == 0) {
    WiFiSM.Set(WiFiIdle);
  }
}

State WiFiFoundStartChar() {
  char buf = wifi.read();
  Serial.println("Found start char");
  for (int line = 0; line < NUM_TRAINLINES; line++) {
    for (int dep = 0; dep < NUM_DEPARTURETIMES; dep++) {
      setTrainTime(line, dep, wifi.parseInt());
    }
  }
  resetUpdateTime();
  
  WiFiSM.Set(WiFiFoundEndChar);

  //  if(buf == '}') {
  //    WiFiSM.Set(WiFiFoundEndChar);
  //  } else {
  //    WiFiString = WiFiString + buf;
  //  }
}

State WiFiFoundEndChar() {
//  Serial.println("Got file:");
//  Serial.println(WiFiString);


  for (int line = 0; line < NUM_TRAINLINES; line++) {
    for (int dep = 0; dep < NUM_DEPARTURETIMES; dep++) {
//      Serial.print("Line ");
//      Serial.print(line);
//      Serial.print(" departure ");
//      Serial.print(dep);
//      Serial.print(" in ");
//      Serial.print(getTrainTime(line, dep));
//      Serial.print(" sec. (");
//      Serial.print(getTrainTime(line, dep)/60);
//      Serial.print(" min)");
//      Serial.println();
    }
  }

  Serial.println("Update done.");
//  Serial.println();

//  WiFiString = "";

  WiFiSM.Set(WiFiIdle);
}
