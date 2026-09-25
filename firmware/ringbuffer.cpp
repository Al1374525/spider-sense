#include <iostream>

const int CAPACITY = 64;

unsigned char buffer[CAPACITY];

int head = 0;

int tail = 0;

int count = 0;

bool push(unsigned char byte){
    if(count == CAPACITY){
        return false;
    }

    buffer[head] = byte; //store byte at head
    head = (head + 1 ) % CAPACITY; // Advance head, wrapping at CAPACITY
    count++; // Increment count

    return true;
}

bool pop(unsigned char* out){
    if(count ==0){
        return false;
    }

    //2. Get the byte at tail
    *out = buffer[tail];

    //3. Advance tail, wrapping around the buffer capacity
    tail = (tail + 1) % CAPACITY;

    //4. Decrement count
    
    count--;

    return true;

}

