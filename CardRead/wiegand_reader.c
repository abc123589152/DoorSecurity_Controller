#include <stdio.h>
#include <wiringPi.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#define D0_PIN 17
#define D1_PIN 18
#define MAX_BITS 32
#define TIMEOUT_MS 100

typedef struct {
    unsigned char data[MAX_BITS/8];
    int bitCount;
    struct timespec lastBitTime;
} WiegandData;

WiegandData wiegandData = {0};

void handleD0(void) {
    if (wiegandData.bitCount < MAX_BITS) {
        wiegandData.data[wiegandData.bitCount / 8] <<= 1;
        wiegandData.bitCount++;
        clock_gettime(CLOCK_MONOTONIC, &wiegandData.lastBitTime);
    }
}

void handleD1(void) {
    if (wiegandData.bitCount < MAX_BITS) {
        wiegandData.data[wiegandData.bitCount / 8] <<= 1;
        wiegandData.data[wiegandData.bitCount / 8] |= 1;
        wiegandData.bitCount++;
        clock_gettime(CLOCK_MONOTONIC, &wiegandData.lastBitTime);
    }
}

void processCard(void) {
    if (wiegandData.bitCount == 26) {
        unsigned int facilityCode = 0;
        unsigned int cardNumber = 0;
        
        // Extract facility code (bits 1-8)
        for (int i = 1; i < 9; i++) {
            facilityCode <<= 1;
            facilityCode |= (wiegandData.data[i/8] >> (7 - (i % 8))) & 1;
        }
        
        // Extract card number (bits 9-24)
        for (int i = 9; i < 25; i++) {
            cardNumber <<= 1;
            cardNumber |= (wiegandData.data[i/8] >> (7 - (i % 8))) & 1;
        }
        
        printf("Facility Code: %u\n", facilityCode);
        printf("Card Number: %u\n", cardNumber);
        
        // Print raw hex data
        printf("Raw Data: ");
        for (int i = 0; i < (wiegandData.bitCount + 7) / 8; i++) {
            printf("%02X", wiegandData.data[i]);
        }
        printf("\n");
    }
    
    // Reset for next card
    memset(wiegandData.data, 0, sizeof(wiegandData.data));
    wiegandData.bitCount = 0;
}

int main(void) {
    if (wiringPiSetupGpio() == -1) {
        fprintf(stderr, "Failed to initialize WiringPi\n");
        return 1;
    }
    
    pinMode(D0_PIN, INPUT);
    pinMode(D1_PIN, INPUT);
    // 啟用內建上拉電阻
    pullUpDnControl(D0_PIN, PUD_UP);
    pullUpDnControl(D1_PIN, PUD_UP);
    wiringPiISR(D0_PIN, INT_EDGE_FALLING, handleD0);
    wiringPiISR(D1_PIN, INT_EDGE_FALLING, handleD1);
    
    printf("Wiegand Reader Started\n");
    
    while (1) {
        struct timespec now;
        clock_gettime(CLOCK_MONOTONIC, &now);
        
        if (wiegandData.bitCount > 0) {
            long ms = (now.tv_sec - wiegandData.lastBitTime.tv_sec) * 1000 +
                     (now.tv_nsec - wiegandData.lastBitTime.tv_nsec) / 1000000;
                     
            if (ms > TIMEOUT_MS) {
                processCard();
            }
        }
        usleep(10000);  // 10ms delay
    }
    
    return 0;
}
