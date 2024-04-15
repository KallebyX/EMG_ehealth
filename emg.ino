# include "eHealth.h"

void setup() {
  Serial.begin(115200);  // Velocidade da porta serial
}

void loop() {
  float emg = eHealth.getEMG();  // Leia o valor EMG
  Serial.println(emg);  // Envie o valor EMG para o computador via serial
  delay(10);  // Delay de 10 milissegundos entre as leituras
}
