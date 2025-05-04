/*
 * linked with -lpthread -lwiringPi -lrt
 */
#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <time.h>
#include <unistd.h>
#include <memory.h>

#define PIN_0 17 // GPIO Pin 17 | Green cable | Data0
#define PIN_1 18 // GPIO Pin 18 | White cable | Data1
#define PIN_SOUND 25 // GPIO Pin 26 | Yellow cable | Sound

#define MAXWIEGANDBITS 32
#define READERTIMEOUT 3000000
#define LEN 256

static unsigned char __wiegandData[MAXWIEGANDBITS];
static unsigned long __wiegandBitCount;
static struct timespec __wiegandBitTime;

void getData0(void) {
    if (__wiegandBitCount / 8 < MAXWIEGANDBITS) {
        __wiegandData[__wiegandBitCount / 8] <<= 1;
        __wiegandBitCount++;
    }
    clock_gettime(CLOCK_MONOTONIC, &__wiegandBitTime);
}

void getData1(void) {
    if (__wiegandBitCount / 8 < MAXWIEGANDBITS) {
        __wiegandData[__wiegandBitCount / 8] <<= 1;
        __wiegandData[__wiegandBitCount / 8] |= 1;
        __wiegandBitCount++;
    }
    clock_gettime(CLOCK_MONOTONIC, &__wiegandBitTime);
}

int wiegandInit(int d0pin, int d1pin) {
    // Setup wiringPi
    //wiringPiSetup() ;
    wiringPiSetupGpio();
    pinMode(d0pin, INPUT);
    pinMode(d1pin, INPUT);
    pinMode(PIN_SOUND, OUTPUT);
    // 啟用內建上拉電阻
    pullUpDnControl(d0pin, PUD_UP);
    pullUpDnControl(d1pin, PUD_UP);
    wiringPiISR(d0pin, INT_EDGE_FALLING, getData0);
    wiringPiISR(d1pin, INT_EDGE_FALLING, getData1);
}

void wiegandReset() {
    memset((void *)__wiegandData, 0, MAXWIEGANDBITS);
    __wiegandBitCount = 0;
}

int wiegandGetPendingBitCount() {
    struct timespec now, delta;
    clock_gettime(CLOCK_MONOTONIC, &now);
    delta.tv_sec = now.tv_sec - __wiegandBitTime.tv_sec;
    delta.tv_nsec = now.tv_nsec - __wiegandBitTime.tv_nsec;

    if ((delta.tv_sec > 1) || (delta.tv_nsec > READERTIMEOUT))
        return __wiegandBitCount;

    return 0;
}

int wiegandReadData(void* data, int dataMaxLen) {
    if (wiegandGetPendingBitCount() > 0) {
        int bitCount = __wiegandBitCount;
        int byteCount = (__wiegandBitCount / 8) + 1;
        memcpy(data, (void *)__wiegandData, ((byteCount > dataMaxLen) ? dataMaxLen : byteCount));       

        wiegandReset();
        return bitCount;
    }
    return 0;
}

void printCharAsBinary(unsigned char ch) {
    int i;
    for (i = 0; i < 8; i++) {
        printf("%d", (ch & 0x80) ? 1 : 0);
        ch <<= 1;
    }
}


void makeBeep(int millisecs, int times){
    int i;
    for (i = 0; i < times; i++) {
        digitalWrite (PIN_SOUND,  LOW);
        delay(millisecs);
        digitalWrite (PIN_SOUND, HIGH);
        delay(millisecs/2);
    }
}
// 加入這個新函數
void printDataAsDecimal(char* data, int bytes) {
    unsigned long long decimal_value = 0;
    
    for (int i = 0; i < bytes; i++) {
        decimal_value = (decimal_value << 8) | (unsigned char)data[i];
    }
    
    printf("%llu", decimal_value);
}
void main(void) {
    int i;

    wiegandInit(PIN_0, PIN_1);


    while(1) {
        int bitLen = wiegandGetPendingBitCount();
        if (bitLen == 0) {
            usleep(5000);
        } else {
           char data[100];
           char string1[100];
           bitLen = wiegandReadData((void *)data, 100);
           int bytes = bitLen / 8 + 1;
           printf("%lu ", (unsigned long)time(NULL));
           printf("Read %d bits (%d bytes): ", bitLen, bytes);
           for (i = 0; i < bytes; i++)
               printf("%02X", (int)data[i]);
           printf(" : ");
           for (i = 0; i < bytes; i++)
               printCharAsBinary(data[i]);
           // 新增：直接輸出十進制數值
           unsigned long long decimal_value = 0;
           for (i = 0; i < bytes; i++) {
               decimal_value = (decimal_value << 8) | (unsigned char)data[i];
           }
           printf(" : %llu", decimal_value);
           makeBeep(200, 1);
        }
    }
}