#include <iostream>
const int CAPACITY = 64;

struct RingBuffer{

    unsigned char buffer[CAPACITY];
    int head;
    int tail;
    int count;
};

void init(RingBuffer* rb){
    rb->head = 0;
    rb->tail =0;
    rb->count = 0;
}

bool push(RingBuffer* rb,unsigned char byte){
    if(rb->count == CAPACITY){
        return false;
    }

   rb->buffer[rb->head] = byte; //store byte at head
    rb->head = (rb->head + 1 ) % CAPACITY; // Advance head, wrapping at CAPACITY
    rb->count++; // Increment count

    return true;
}

bool pop(RingBuffer* rb,  unsigned char* out){
    if(rb->count ==0){
        return false;
    }

    //2. Get the byte at tail
    *out = rb->buffer[rb->tail];

    //3. Advance tail, wrapping around the buffer capacity
    rb->tail = (rb->tail + 1) % CAPACITY;

    //4. Decrement count
    
    rb->count--;

    return true;

}

int main(){
    RingBuffer rb;
    init(&rb);
    unsigned char value;

    std::cout << "--- basic push/pop --\n";

   
   push(&rb, 10);
   push(&rb, 20);
   push(&rb, 30);
    
    while(pop(&rb, &value)){
        std::cout << (int)value << "\n";
    }

    std::cout << "--- wraparound ---\n";

    for(int i = 0; i < 64;i++){
        push(&rb, (unsigned char)i);
    }

    for (int i =0; i < 32; i++){
        pop(&rb, &value);
    }

    for(int i= 100; i <132; i++){
        push(&rb, (unsigned char)i);
    }

        while (pop(&rb, &value)) {
        std::cout << (int)value << " ";
    }


    std::cout << "\n";
}

