#include <wiringPi.h>
int main(void){
  // uses BCM numbering of the GPIOs and directly accesses the GPIO registers.
  wiringPiSetupGpio();

  // pin mode ..(INPUT, OUTPUT, PWM_OUTPUT, GPIO_CLOCK)
  // set pin 17 to input
  pinMode(17, OUTPUT);
  while(1){
    digitaWrite(17,HIGH);
    delay(500);
    digitaWrite(17,LOW);
    delay(500);
  }
}