#include <Arduino.h>

#define TAG "RS485_ECHO_APP"
#define ECHO_TEST_TXD 17
#define ECHO_TEST_RXD 16
#define ECHO_TEST_RE 2
#define ECHO_TEST_DE 4
#define BUF_SIZE  127
#define PACKET_READ_TICS   100 // (100 / portTICK_PERIOD_MS)
#define ECHO_READ_TOUT 3

// Modbus RTU requests for reading NPK values
char nitro[] = {0xFF, 0x03, 0x00, 0x00, 0x00, 0x01, 0x91, 0xD4};
char phos[]  = {0x01, 0x03, 0x00, 0x1F, 0x00, 0x01, 0xB5, 0x0C};
char pota[]  = {0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0x0C};

// A byte array to store NPK values
byte values[11];
byte data[BUF_SIZE];
int recvdCount = 0;

static void echo_send(const char* str, uint8_t length) {
  digitalWrite(ECHO_TEST_DE, HIGH);
  digitalWrite(ECHO_TEST_RE, HIGH);
  if (Serial2.write(str, length) != length) {
    Serial.println("Send data critical failure.");
    abort();
  } else Serial2.flush();

  digitalWrite(ECHO_TEST_DE, LOW);
  digitalWrite(ECHO_TEST_RE, LOW);
}

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600, SERIAL_8N1, ECHO_TEST_RXD, ECHO_TEST_TXD);
  pinMode(ECHO_TEST_RE, OUTPUT);
  pinMode(ECHO_TEST_DE, OUTPUT);
  echo_send("Start RS485 UART test.\r\n", 24);
  Serial.println("Ready..");
}

void loop() {
  unsigned long now = millis();

  if (Serial2.available()) {
    recvdCount = 0;
    memset(data, 0, sizeof(data));
    while (millis() - now < PACKET_READ_TICS) {
      if (Serial2.available()) {
        byte b = Serial2.read();
        data[recvdCount] = b;
        recvdCount++;
        if (recvdCount >= sizeof(data)) {
          recvdCount = 0;
        }
      }
    }

    if (recvdCount > 0) {
      echo_send("\r\n", 2);
      char prefix[] = "RS485 Received: [";
      echo_send(prefix, (sizeof(prefix) - 1));
      Serial.print("Esp Received: ");
      echo_send(prefix, (sizeof(prefix) - 1));
      for (int i = 0; i < recvdCount; i++) {
        Serial.printf("0x%.2X ", (uint8_t)data[i]);
        Serial.print("; Echo Sent: ");
        echo_send((const char*)&data[i], 1);
        if (data[i] == '\r') {
          echo_send("\n", 1);
        }
      }
      echo_send("]\r\n", 3);
    } else {
      echo_send(".", 1);
      Serial.println(".");
    }

    if (data[recvdCount - 1] == ';') {
      echo_send("\r\n", 2);
      Serial.print("Esp Received: ");
      echo_send(nitro, (sizeof(nitro) - 1));
      echo_send(phos, (sizeof(phos) - 1));
      echo_send(pota, (sizeof(pota) - 1));

      int nitroValue, phosValue, potaValue;
      if (sscanf((const char*)data, "N:%d;P:%d;K:%d;", &nitroValue, &phosValue, &potaValue) == 3) {
        for (int i = 0; i < recvdCount; i++) {
          Serial.printf("0x%.2X ", (uint8_t)data[i]);
          Serial.print("; Echo Sent: ");
          Serial.print(" | Nitrogen: ");
          Serial.print(nitroValue);
          Serial.print(" | Phosphorus: ");
          Serial.print(phosValue);
          Serial.print(" | Potassium: ");
          Serial.println(potaValue);
          echo_send((const char*)&data[i], 1);
          if (data[i] == '\r') {
            echo_send("\n", 1);
          }
        }
        echo_send("]\r\n", 3);
      } else {
        Serial.println("Error: Failed to parse NPK sensor data");
      }

      memset(data, 0, sizeof(data));
      recvdCount = 0;
    }
  }
}

byte readValue(const byte* request, byte requestSize) {
  digitalWrite(ECHO_TEST_RE, HIGH);
  digitalWrite(ECHO_TEST_DE, HIGH);

  Serial2.write(request, requestSize);

  digitalWrite(ECHO_TEST_RE, LOW);
  digitalWrite(ECHO_TEST_DE, LOW);

  delay(100); // Adjust the delay as needed

  byte responseLength = Serial2.available();
  for (byte i = 0; i < responseLength; i++) {
    values[i] = Serial2.read();
  }

  Serial.print("Response Length: ");
  Serial.println(responseLength);

  Serial.print("Received Bytes: ");
  for (byte i = 0; i < responseLength; i++) {
    Serial.print(values[i], HEX);
    Serial.print(" ");
  }
  Serial.println();

  return values[3] << 8 | values[4];
}
