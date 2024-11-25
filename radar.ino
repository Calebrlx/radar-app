// Constants for serial communication
#define RADAR_BAUDRATE 256000  // Radar module's baud rate
#define DEBUG_BAUDRATE 115200  // Debugging baud rate

// Buffer size for incoming data
#define BUFFER_SIZE 32

void setup() {
  // Initialize serial communication with the radar module
  Serial.begin(RADAR_BAUDRATE);  // Use Serial for radar communication
  while (!Serial);               // Wait for Serial to be ready

  // Initialize debugging serial communication
  Serial1.begin(DEBUG_BAUDRATE); // Use Serial1 for debugging via USB
  while (!Serial1);

  Serial1.println("Radar Module Decoder Initialized.");
}

void loop() {
  // Check if radar data is available
  if (Serial.available()) {
    uint8_t buffer[BUFFER_SIZE];
    size_t length = Serial.readBytes(buffer, BUFFER_SIZE); // Read incoming data into buffer

    // Decode and print radar data
    decodeAndPrint(buffer, length);
  }
}

/**
 * Decodes and prints radar data.
 * @param buffer The raw data buffer.
 * @param length The length of the buffer.
 */
void decodeAndPrint(uint8_t* buffer, size_t length) {
  if (length < 10) {
    Serial1.println("Insufficient data received.");
    return;
  }

  // Decode the radar data
  uint16_t angle = (buffer[5] << 8) | buffer[4];          // Bytes 4-5: Angle (little-endian)
  uint16_t distance = (buffer[7] << 8) | buffer[6];       // Bytes 6-7: Distance (little-endian)
  uint16_t speed = (buffer[9] << 8) | buffer[8];          // Bytes 8-9: Speed/Trajectory (little-endian)

  // Print raw data in hex format
  Serial1.print("Raw Data (Hex): ");
  for (size_t i = 0; i < length; i++) {
    if (i > 0) Serial1.print(" ");
    Serial1.print(buffer[i], HEX);
  }
  Serial1.println();

  // Print decoded data
  Serial1.print("Decoded Data: ");
  Serial1.print("Angle: ");
  Serial1.print(angle);
  Serial1.print(" | Distance (mm): ");
  Serial1.print(distance);
  Serial1.print(" | Speed (mm/s): ");
  Serial1.println(speed);
}