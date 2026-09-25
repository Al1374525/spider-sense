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

int main(){
    unsigned char value;

    std::cout << "--- basic push/pop --\n";

    push(10);
    push(20);
    push(30);
    
    while(pop(&value)){
        std::cout << (int)value << "\n";
    }

    std::cout << "--- wraparound ---\n";

    for(int i = 0; i < 64;i++){
        push((unsigned char)i);
    }

    for (int i =0; i < 32; i++){
        pop(&value);
    }

    for(int i= 100; i <132; i++){
        push((unsigned char)i);
    }

    while (pop(&value)){
        std::cout << (int)value << " ";
    }

    std::cout << "\n";
}

